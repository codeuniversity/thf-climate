from typing import List, Optional

from pydantic import BaseModel

from src.constants import AggregationMethod, LocationName, TemporalResolution, Unit, IndexType


class DataPoint(BaseModel):
    value: float
    timestamp: Optional[int]  # UNIX timestamp in seconds or nan


class BaseMeta(BaseModel):
    location: LocationName
    startDate: int
    endDate: int
    temporalResolution: TemporalResolution
    aggregation: AggregationMethod


class TemperatureMetaResponse(BaseMeta):
    unit: Unit = Unit.CELSIUS


class TemperatureResponse(BaseModel):
    meta: TemperatureMetaResponse
    data: List[DataPoint]


class NDVIMetaResponse(BaseMeta):
    indexType: IndexType = IndexType.NDVI
    unit: Unit = Unit.NORMALIZED_DIFFERENCE


class NDVIResponse(BaseMeta):
    meta: NDVIMetaResponse
    data: List[DataPoint]

class MSAVIMetaResponse(BaseMeta):
    indexType: IndexType = IndexType.MSAVI
    unit: Unit = Unit.DIMENSIONLESS

class MSAVIResponse(BaseMeta):
    meta: MSAVIMetaResponse
    data: List[DataPoint]