from datetime import datetime

import pandas as pd

from src.constants import AggregationMethod, LocationPolygon, TemporalResolution
from src.gee.index import get_preprocessed_imagery
from src.gee.ndvi import get_ndvi_info


def aggregate_time_series(
    ndvi_info: list[dict],
    temporal_resolution: TemporalResolution,
    aggregation_method: AggregationMethod,
):
    # Create a DataFrame from the ndvi_info list
    df = pd.DataFrame(ndvi_info)

    # Set the timestamp as the DataFrame index
    df.set_index("timestamp", inplace=True)

    # Resample the DataFrame based on the temporal resolution
    if temporal_resolution == TemporalResolution.DAILY:
        resampled_df = df.resample("D")
    elif temporal_resolution == TemporalResolution.MONTHLY:
        resampled_df = df.resample("M")
    else:
        raise ValueError("Unsupported temporal resolution")

    # Aggregate the resampled DataFrame based on the aggregation method
    if aggregation_method == AggregationMethod.MEAN:
        aggregated_df = resampled_df.mean()
    elif aggregation_method == AggregationMethod.MIN:
        aggregated_df = resampled_df.min()
    elif aggregation_method == AggregationMethod.MIN:
        aggregated_df = resampled_df.max()
    elif aggregation_method == AggregationMethod.MEDIAN:
        aggregated_df = resampled_df.median()
    else:
        raise ValueError("Unsupported aggregation method")

    # Convert the aggregated DataFrame back to a list of dicts
    aggregated_info = aggregated_df.reset_index().to_dict(orient="records")
    for record in aggregated_info:
        print(f"Timestamp: {record['timestamp']}, VALUE: {record['value']}")

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
        NDVI_time_series, temporal_resolution, aggregation_method
    )
    return aggregated_data_dict
