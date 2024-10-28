from fastapi import APIRouter, Query

from src.constants import AggregationMethod, LocationName, TemporalResolution
from src.validation.models import (
    DataPoint,
    TemperatureMetaResponse,
    TemperatureResponse,
)
from src.validation.utils import (
    validate_timestamp_in_range,
    validate_timestamp_start_date_before_end_date,
)

weather_router = APIRouter()


@weather_router.get("/temp", response_model=TemperatureResponse)
async def get_temperature_data(
    startDate: int = Query(..., description="Start date as UNIX timestamp in seconds"),
    endDate: int = Query(..., description="End date as UNIX timestamp in seconds"),
    location: LocationName = Query(..., description="Location name"),
    temporalResolution: TemporalResolution = Query(
        ..., description="Temporal resolution"
    ),
    aggregation: AggregationMethod = Query(..., description="Aggregation method"),
):
    validate_timestamp_in_range(startDate)
    validate_timestamp_in_range(endDate)
    validate_timestamp_start_date_before_end_date(startDate, endDate)

    # do the real processing here :)

    # just a dummy response for now
    sample_response = TemperatureResponse(
        meta=TemperatureMetaResponse(
            unit="Celsius",
            location=location,
            startDate=startDate,
            endDate=endDate,
            temporalResolution=temporalResolution,
            aggregation=aggregation,
        ),
        data=[
            DataPoint(value=13.45, timestamp=1617321600),
            DataPoint(value=15.5, timestamp=1617555600),
            DataPoint(value=24.0, timestamp=1677721600),
        ],
    )
    return sample_response
