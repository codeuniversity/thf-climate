from enum import Enum


class AggregationMethod(str, Enum):
    MEAN = "MEAN"
    MEDIAN = "MEDIAN"
    MAX = "MAX"
    MIN = "MIN"


class TemporalResolution(str, Enum):
    DAILY = "DAILY"
    MONTHLY = "MONTHLY"


class LocationName(str, Enum):
    TEMPELHOFER_FELD = "TEMPELHOFER-FELD"


class IndexType(str, Enum):
    NDVI = "NDVI"
    MSAVI = "MSAVI"
    GNDVI = "GNDVI"


class Unit(str, Enum):
    CELSIUS = "Celsius"
