import math
from datetime import datetime

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from src.constants import (
    AggregationMethod,
    LocationName,
    TemporalResolution,
    Unit,
)
from src.service import ndvi_service
from src.utils.temporal import get_optimistic_rounding
from src.validation.models import NDVIResponse
from src.validation.utils import (
    validate_timestamp_in_range,
    validate_timestamp_start_date_before_end_date,
)

ndvi_router = APIRouter()


@ndvi_router.get("/ndvi", response_model=NDVIResponse)
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

    start_date_dt = datetime.utcfromtimestamp(startDate)
    end_date_dt = datetime.utcfromtimestamp(endDate)

    rounded_start_date, rounded_end_date = get_optimistic_rounding(
        start_date_dt, end_date_dt, temporalResolution
    )

    data = ndvi_service(
        location=location,
        temporal_resolution=temporalResolution,
        aggregation_method=aggregation,
        start_date=rounded_start_date,
        end_date=rounded_end_date,
    )

    # Ensure all timestamps are converted to integers (UNIX timestamps)
    formatted_data = [
        {
            "timestamp": int(dp["timestamp"].timestamp()),
            "value": None if math.isnan(dp["value"]) else dp["value"],
        }
        for dp in data
    ]
    response = {
        "meta": {
            "location": LocationName[location].value,
            "startDate": int(rounded_start_date.timestamp()),
            "endDate": int(rounded_end_date.timestamp()),
            "temporalResolution": TemporalResolution[temporalResolution].value,
            "aggregation": AggregationMethod[aggregation].value,
            "unit": Unit.NORMALIZED_DIFFERENCE.value,
        },
        "data": formatted_data,
    }

    print(response)
    return JSONResponse(content=response)
