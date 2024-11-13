from datetime import datetime

import pandas as pd

from src.constants import AggregationMethod, LocationPolygon, TemporalResolution
from src.gee.index import get_preprocessed_imagery
from src.gee.ndvi import get_ndvi_info


def aggregate_time_series(
    ndvi_info: list[dict],
    temporal_resolution,
    aggregation_method,
    start_date: datetime,
    end_date: datetime,
):
    # Generate a complete date range based on temporal resolution
    if temporal_resolution == "DAILY":
        date_range = pd.date_range(start=start_date, end=end_date, freq="D", tz="UTC")
    elif temporal_resolution == "MONTHLY":
        date_range = pd.date_range(start=start_date, end=end_date, freq="MS", tz="UTC")
    else:
        raise ValueError("Unsupported temporal resolution")

    # Create a DataFrame with the full date range, initially filled with None
    df = pd.DataFrame(index=date_range)
    df.index.name = "timestamp"
    df["value"] = None

    # Convert ndvi_info to a DataFrame and set the index
    if temporal_resolution == "MONTHLY":
        for record in ndvi_info:
            record["timestamp"] = record["timestamp"].replace(day=1)
    info_df = pd.DataFrame(ndvi_info)
    info_df["timestamp"] = pd.to_datetime(info_df["timestamp"], unit="s", utc=True)

    # Align info_df to the temporal resolution
    if temporal_resolution == "DAILY":
        info_df["timestamp"] = info_df["timestamp"].dt.floor("D")
    elif temporal_resolution == "MONTHLY":
        info_df["timestamp"] = info_df["timestamp"].dt.to_period("M").dt.to_timestamp()

    info_df.set_index("timestamp", inplace=True)

    # Update the full DataFrame with actual NDVI values
    df.loc[info_df.index, "value"] = info_df["value"]

    # Resample the DataFrame based on the temporal resolution
    resampled_df = (
        df.resample("D") if temporal_resolution == "DAILY" else df.resample("M")
    )

    # Aggregate the resampled DataFrame based on the aggregation method, ignoring None values
    if aggregation_method == "MEAN":
        aggregated_df = resampled_df.mean()
    elif aggregation_method == "MIN":
        aggregated_df = resampled_df.min()
    elif aggregation_method == "MAX":
        aggregated_df = resampled_df.max()
    elif aggregation_method == "MEDIAN":
        aggregated_df = resampled_df.median()
    else:
        raise ValueError("Unsupported aggregation method")

    # Replace NaNs with None for final output consistency
    aggregated_df = aggregated_df.where(pd.notnull(aggregated_df), None)

    # Convert the aggregated DataFrame back to a list of dicts with ISO format timestamps
    aggregated_info = [
        {"timestamp": record["timestamp"].isoformat(), "value": record["value"]}
        for record in aggregated_df.reset_index().to_dict(orient="records")
    ]

    return aggregated_info


def ndvi_service(
    location: LocationPolygon,
    temporal_resolution: TemporalResolution,
    aggregation_method: AggregationMethod,
    start_date: datetime,
    end_date: datetime,
):
    masked_images = get_preprocessed_imagery(
        LocationPolygon[location.value].value,
        start_date,
        end_date,
    )
    NDVI_time_series = get_ndvi_info(
        masked_images, LocationPolygon[location.value].value
    )
    aggregated_data_dict = aggregate_time_series(
        NDVI_time_series, temporal_resolution, aggregation_method, start_date, end_date
    )
    return aggregated_data_dict
