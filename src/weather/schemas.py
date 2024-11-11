from typing import List
from enum import Enum
from pydantic import BaseModel, Field, ValidationInfo, field_validator

from src.constants import AggregationMethod, LocationName, TemporalResolution, Unit
from src.validation.utils import (
    validate_timestamp_in_range,
    validate_timestamp_start_date_before_end_date,
)

class WeatherVariable(str, Enum):
    TEMPERATURE = "temperature_2m"
    HUMIDITY = "relative_humidity_2m"
    PRECIPITATION = "precipitation"
    SOIL_TEMPERATURE = "soil_temperature_0_to_7cm"
    SOIL_MOISTURE = "soil_moisture_0_to_7cm"

class WeatherVariableUnit(str, Enum):
    temperature_2m = "Celsius"
    soil_temperature_0_to_7cm = "Celsius"
    relative_humidity_2m = "%"
    precipitation = "mm"
    soil_moisture_0_to_7cm = "m³/m³"

# Request for getting the temperature data
class WeatherDataRequest(BaseModel):
    weatherVariable: WeatherVariable = Field(..., description="The weather variable to fetch the weather data")
    startDate: int = Field(..., description="Start date as UNIX timestamp in seconds")
    endDate: int = Field(..., description="End date as UNIX timestamp in seconds")
    location: LocationName = Field(..., description="Location name")
    temporalResolution: TemporalResolution = Field(
        ..., description="Temporal resolution"
    )
    aggregation: AggregationMethod = Field(..., description="Aggregation method")

    # Custom validator to check if timestamps are valid and in the correct order
    @field_validator("startDate")
    def validate_timestamp_in_range(cls, v):
        return validate_timestamp_in_range(v)

    @field_validator("endDate")
    def end_date_must_be_after_start_date(cls, v, info: ValidationInfo):
        return validate_timestamp_start_date_before_end_date(
            info.data.get("startDate"), v
        )

class WeatherDataMeta(BaseModel):
    weatherVariable: str
    unit: str
    startDate: int
    endDate: int
    unit: Unit
    location: LocationName
    temporalResolution: TemporalResolution
    aggregation: AggregationMethod


class DataPoint(BaseModel):
    value: float
    timestamp: int


class WeatherDataResponse(BaseModel):
    meta: WeatherDataMeta
    data: List[DataPoint]
