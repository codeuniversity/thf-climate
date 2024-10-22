from typing import List

from pydantic import BaseModel

from src.constants import AggregationMethod, LocationName, TemporalResolution, Unit


class DataPoint(BaseModel):
    value: float
    timestamp: int  # UNIX timestamp in seconds


class BaseMeta(BaseModel):
    location: LocationName
    startDate: int
    endDate: int
    temporalResolution: TemporalResolution
    aggregation: AggregationMethod


class TemperatureDataMeta(BaseMeta):
    unit: Unit = Unit.CELSIUS


class TemperatureDataResponse(BaseModel):
    meta: TemperatureDataMeta
    data: List[DataPoint]
