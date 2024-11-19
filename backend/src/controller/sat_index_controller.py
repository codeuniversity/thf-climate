from datetime import datetime, timezone

from fastapi import Query
from fastapi.responses import JSONResponse
from src.constants import (
    IndexType,
    AggregationMethod,
    LocationName,
    TemporalResolution,
    Unit,
)
from src.service import ndvi_service
from src.utils.temporal import get_optimistic_rounding
from src.validation.utils import (
    validate_timestamp_in_range_of_S2_imagery,
    validate_timestamp_start_date_before_end_date,
)


async def sat_index_controller(
    sat_index_type: IndexType, 
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

    data = ndvi_service(
        location=location,
        temporal_resolution=temporalResolution,
        aggregation_method=aggregation,
        start_date=rounded_start_date,
        end_date=rounded_end_date,
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