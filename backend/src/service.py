from datetime import datetime, timezone, timedelta

import pandas as pd

from src.constants import AggregationMethod, LocationPolygon, TemporalResolution
from src.gee.image_preprocessing import get_preprocessed_imagery
from src.gee.sat_index_info import get_sat_index_info
from src.gee.ndvi_cache import ndvi_daily_cache
from typing import List, Dict, Union
import math


def initialize_time_series(
    time_series: List[Dict[str, Union[int, float]]],
    temporal_resolution: TemporalResolution,
    aggregation_method: AggregationMethod
) -> pd.DataFrame:
    """
    Initializes a pandas DataFrame from a time series and applies temporal resolution and aggregation.

    Parameters:
        time_series (List[Dict[str, Union[int, float]]]): List of dicts with 'timestamp' and 'value'.
        temporal_resolution (TemporalResolution): Temporal resolution, either DAILY or MONTHLY.
        aggregation_method (AggregationMethod): Aggregation method to use if resolution is MONTHLY.

    Returns:
        pd.DataFrame: The resulting DataFrame with applied resolution and aggregation.
    """
    # Check if the time_series is empty
    if not time_series:
        # Return an empty DataFrame with a datetime index and 'value' column in UTC
        if temporal_resolution == TemporalResolution.MONTHLY:
            empty_index = pd.date_range(
                start="1970-01-01", periods=0, freq='MS', tz='UTC')
        else:
            empty_index = pd.date_range(
                start="1970-01-01", periods=0, freq='D', tz='UTC')

        return pd.DataFrame(index=empty_index, columns=['value'])

    # Convert timestamps to datetime in UTC and create DataFrame
    df = pd.DataFrame(time_series)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
    df.set_index('timestamp', inplace=True)

    # Resample based on temporal resolution and apply aggregation if needed
    if temporal_resolution == TemporalResolution.MONTHLY:
        if aggregation_method == AggregationMethod.MEAN:
            df = df.resample('MS').mean()
        elif aggregation_method == AggregationMethod.MEDIAN:
            df = df.resample('MS').median()
        elif aggregation_method == AggregationMethod.MAX:
            df = df.resample('MS').max()
        elif aggregation_method == AggregationMethod.MIN:
            df = df.resample('MS').min()
    # If DAILY, do nothing as time series is already in daily format
    return df


def fill_missing_dates(
    df: pd.DataFrame,
    start: datetime,
    end: datetime,
    temporal_resolution: TemporalResolution
) -> pd.DataFrame:
    """
    Fills missing entries in the time series, adding NaN for missing days or months.

    Parameters:
        df (pd.DataFrame): Input DataFrame with timestamps as index.
        start (datetime): Start datetime for filling.
        end (datetime): End datetime for filling.
        temporal_resolution (TemporalResolution): Temporal resolution, either DAILY or MONTHLY.

    Returns:
        pd.DataFrame: DataFrame with missing dates or months filled with NaN values.
    """
    # Ensure start and end are in UTC
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    else:
        start = start.astimezone(timezone.utc)

    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    else:
        end = end.astimezone(timezone.utc)

    # Generate the complete date range based on the temporal resolution
    if temporal_resolution == TemporalResolution.DAILY:
        date_range = pd.date_range(start=start, end=end, freq='D', tz='UTC')
    elif temporal_resolution == TemporalResolution.MONTHLY:
        date_range = pd.date_range(start=start, end=end, freq='MS', tz='UTC')
    # If the input DataFrame is empty, create a new one with NaNs for all dates in the range
    if df.empty:
        df = pd.DataFrame(index=date_range, columns=['value'])
        df['value'] = None
    else:
        # Reindex to the complete date range, filling missing dates with NaN
        df = df.reindex(date_range)

    df.columns = ['value']
    return df


def ndvi_service(
    location: LocationPolygon,
    temporal_resolution: TemporalResolution,
    aggregation_method: AggregationMethod,
    start_date: datetime,
    end_date: datetime,
):
    # Temporary implementation of GEE Caching strategy
    current_cache_end_date = datetime(
        2024, 9, 29, tzinfo=timezone.utc)
    if start_date < current_cache_end_date and end_date < current_cache_end_date:  # current end of cache
        cache_start_date = start_date
        cache_end_date = end_date
        processing_start_date = None
        processing_end_date = None

    elif start_date < current_cache_end_date and end_date > current_cache_end_date:
        cache_start_date = start_date
        cache_end_date = current_cache_end_date
        processing_start_date = current_cache_end_date + timedelta(days=1)
        processing_end_date = end_date

    elif start_date > current_cache_end_date:
        cache_start_date = None
        cache_end_date = None
        processing_start_date = start_date
        processing_end_date = end_date

    if processing_start_date:

        masked_images = get_preprocessed_imagery(
            LocationPolygon[location.value].value,
            processing_start_date,
            processing_end_date,
        )
        NDVI_time_series = get_sat_index_info(
            masked_images, LocationPolygon[location.value].value
        )

    if cache_start_date:
        cached_data_subset = get_cache_subset(cache_start_date, cache_end_date)

    if processing_start_date and cache_start_date:
        ndvi_data = cached_data_subset + NDVI_time_series
    else:
        ndvi_data = cached_data_subset if cache_start_date else NDVI_time_series

    index_df = initialize_time_series(
        ndvi_data, temporal_resolution, aggregation_method)

    filled_df = fill_missing_dates(
        index_df, start_date, end_date, temporal_resolution)

    return convert_df_to_list(filled_df)


def get_cache_subset(start_date: datetime, end_date: datetime):
    subset: list[dict] = []
    for entry in ndvi_daily_cache:
        if entry["timestamp"] >= int(start_date.timestamp()) and entry["timestamp"] <= int(end_date.timestamp()):
            subset.append(entry)
    return subset


def convert_df_to_list(df: pd.DataFrame) -> List[Dict[str, Union[int, float, None]]]:
    """
    Converts a DataFrame with a datetime index back to a list of dictionaries in the original format.

    Parameters:
        df (pd.DataFrame): Input DataFrame with datetime index and a 'value' column.

    Returns:
        List[Dict[str, Union[int, float, None]]]: List of dictionaries with 'timestamp' in epoch format and 'value'.
    """
    # Convert the DataFrame index to epoch timestamps and reset index
    df_reset = df.reset_index()
    df_reset['timestamp'] = df_reset['index'].astype(int) // 10**9
    df_reset = df_reset.rename(columns={'value': 'value'})

    # Convert to list of dictionaries
    result = df_reset[['timestamp', 'value']].to_dict(orient='records')

    # Convert NaN to None (needs to handle empty df as well)
    for entry in result:
        if entry['value'] is None:
            entry['value'] = None
        elif math.isnan(entry['value']):
            entry['value'] = None

    return result
