import pytest
from datetime import datetime
from src.service import aggregate_time_series
from src.constants import AggregationMethod, TemporalResolution

def test_aggregate_time_series_daily_mean():
    ndvi_info = [
        {"timestamp": 1633046400, "value": 0.5},
        {"timestamp": 1633132800, "value": 0.6}
    ]
    start_date = datetime(2021, 10, 1)
    end_date = datetime(2021, 10, 2)
    result = aggregate_time_series(
        ndvi_info, TemporalResolution.DAILY, AggregationMethod.MEAN, start_date, end_date
    )
    assert len(result) == 2
    assert result[0]["value"] == 0.5
    assert result[1]["value"] == 0.6

def test_aggregate_time_series_monthly_max():
    ndvi_info = [
        {"timestamp": 1633046400, "value": 0.5},
        {"timestamp": 1635724800, "value": 0.7}
    ]
    start_date = datetime(2021, 10, 1)
    end_date = datetime(2021, 11, 30)
    result = aggregate_time_series(
        ndvi_info, TemporalResolution.MONTHLY, AggregationMethod.MAX, start_date, end_date
    )
    assert len(result) == 2
    assert result[0]["value"] == 0.5
    assert result[1]["value"] == 0.7