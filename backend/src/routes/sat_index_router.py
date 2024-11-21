from datetime import datetime, timezone

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from src.constants import (
    AggregationMethod,
    LocationName,
    TemporalResolution,
    Unit,
    IndexType
)
from src.service import sat_index_service
from src.utils.temporal import get_optimistic_rounding
from src.validation.models import NDVIResponse, MSAVIResponse
from src.validation.utils import (
    validate_timestamp_in_range_of_S2_imagery,
    validate_timestamp_start_date_before_end_date,
)

sat_index_router = APIRouter()


@sat_index_router.get("/ndvi", response_model=NDVIResponse)
async def get_ndvi_data(
    startDate: int = Query(...,
                           description="Start date as UNIX timestamp in seconds"),
    endDate: int = Query(...,
                         description="End date as UNIX timestamp in seconds"),
    location: LocationName = Query(..., description="Location name"),
    temporalResolution: TemporalResolution = Query(
        ..., description="Temporal resolution"
    ),
    aggregation: AggregationMethod = Query(...,
                                           description="Aggregation method"),
):

    validate_timestamp_start_date_before_end_date(startDate, endDate)
    validate_timestamp_in_range_of_S2_imagery(startDate, endDate)
    start_date_dt = datetime.fromtimestamp(startDate, tz=timezone.utc)
    end_date_dt = datetime.fromtimestamp(endDate, tz=timezone.utc)

    rounded_start_date, rounded_end_date = get_optimistic_rounding(
        start_date_dt, end_date_dt, temporalResolution
    )

    data = sat_index_service(
        location=location,
        temporal_resolution=temporalResolution,
        aggregation_method=aggregation,
        start_date=rounded_start_date,
        end_date=rounded_end_date,
        index_type=IndexType.NDVI
    )

    response = {
        "meta": {
            "location": LocationName[location].value,
            "startDate": int(rounded_start_date.timestamp()),
            "endDate": int(rounded_end_date.timestamp()),
            "temporalResolution": TemporalResolution[temporalResolution].value,
            "aggregation": AggregationMethod[aggregation].value,
            "unit": Unit.NORMALIZED_DIFFERENCE.value,
        },
        "data": data,
    }

    return JSONResponse(content=response)

@sat_index_router.get("/msavi", response_model=MSAVIResponse)
async def get_msavi_data(
    startDate: int = Query(...,
                           description="Start date as UNIX timestamp in seconds"),
    endDate: int = Query(...,
                         description="End date as UNIX timestamp in seconds"),
    location: LocationName = Query(..., description="Location name"),
    temporalResolution: TemporalResolution = Query(
        ..., description="Temporal resolution"
    ),
    aggregation: AggregationMethod = Query(...,
                                           description="Aggregation method"),
):

    validate_timestamp_start_date_before_end_date(startDate, endDate)
    validate_timestamp_in_range_of_S2_imagery(startDate, endDate)
    start_date_dt = datetime.fromtimestamp(startDate, tz=timezone.utc)
    end_date_dt = datetime.fromtimestamp(endDate, tz=timezone.utc)

    rounded_start_date, rounded_end_date = get_optimistic_rounding(
        start_date_dt, end_date_dt, temporalResolution
    )

    data = sat_index_service(
        location=location,
        temporal_resolution=temporalResolution,
        aggregation_method=aggregation,
        start_date=rounded_start_date,
        end_date=rounded_end_date,
        index_type=IndexType.MSAVI
    )

    response = {
        "meta": {
            "location": LocationName[location].value,
            "startDate": int(rounded_start_date.timestamp()),
            "endDate": int(rounded_end_date.timestamp()),
            "temporalResolution": TemporalResolution[temporalResolution].value,
            "aggregation": AggregationMethod[aggregation].value,
            "unit": Unit.NORMALIZED_DIFFERENCE.value,
        },
        "data": data,
    }

    return JSONResponse(content=response)