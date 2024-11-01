from datetime import datetime
from fastapi import APIRouter, Query
from pytz import timezone

from src.constants import (
    AggregationMethod,
    TemporalResolution,
    LocationName,
    LocationPolygon,
    IndexType,
    Unit,
)
from src.utils.temporal import get_optimistic_rounding
from src.validation.utils import (
    validate_timestamp_in_range,
    validate_timestamp_start_date_before_end_date,
)

msavi_router = APIRouter()


@msavi_router.get("/msavi")
def get_msavi(
    startDate: int = Query(
        ...,
        description="Beginning of requested date range in UNIX timestamp as seconds",
    ),
    endDate: int = Query(
        ..., description="End of requested date range in UNIX timestamp as seconds"
    ),
    location: LocationName = Query(..., description="Name of the requested location"),
    temporalResolution: TemporalResolution = Query(
        ...,
        description="Time interval that a single data point should represent e.g. one month",
    ),
    aggregation: AggregationMethod = Query(
        ...,
        description="Method of aggregating available data into a single datapoint to represent the selected time interval e.g. mean average",
    ),
):
    validate_timestamp_in_range(startDate)
    validate_timestamp_in_range(endDate)
    validate_timestamp_start_date_before_end_date(startDate, endDate)

    start_datetime = datetime.fromtimestamp(startDate, timezone.utc)
    end_datetime = datetime.fromtimestamp(endDate, timezone.utc)

    rounded_start_date, rounded_end_date = get_optimistic_rounding(
        start_datetime, end_datetime, temporalResolution
    )

    data = {}  # TODO: return dynamic data

    return {
        "meta": {
            "index": IndexType.MSAVI,
            "location": LocationName[location].value,
            "startDate": startDate,
            "endDate": endDate,
            "temporalResolution": TemporalResolution[temporalResolution].value,
            "aggregation": AggregationMethod[aggregation].value,
        },
        "data": data,
    }
