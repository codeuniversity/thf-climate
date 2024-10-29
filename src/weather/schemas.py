from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List
from src.constants import AggregationMethod, LocationName, TemporalResolution, Unit
from src.validation.utils import (
    validate_timestamp_in_range,
    validate_timestamp_startdate_before_enddate,
)

# Request for getting the temperature data
class TemperatureDataRequest(BaseModel):
    startDate: int = Field(..., description="Start date as UNIX timestamp in seconds")
    endDate: int = Field(..., description="End date as UNIX timestamp in seconds")
    location: LocationName = Field(..., description="Location name")
    temporalResolution: TemporalResolution = Field(..., description="Temporal resolution")
    aggregation: AggregationMethod = Field(..., description="Aggregation method")

    # Custom validator to check if timestamps are valid and in the correct order
    @field_validator("startDate")
    def validate_timestamp_in_range(cls, v):
        return validate_timestamp_in_range(v)

    @field_validator("endDate")
    def end_date_must_be_after_start_date(cls, v, info: ValidationInfo):
        return validate_timestamp_startdate_before_enddate(info.data.get("startDate"), v)

class TemperatureDataMeta(BaseModel):
    startDate: int
    endDate: int
    unit: Unit
    location: LocationName
    temporalResolution: TemporalResolution
    aggregation: AggregationMethod

class DataPoint(BaseModel):
    value: float
    timestamp: int

class TemperatureDataResponse(BaseModel):
    meta: TemperatureDataMeta
    data: List[DataPoint]
