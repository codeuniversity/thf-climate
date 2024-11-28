import pytest
from datetime import datetime, timezone
from src.utils.temporal import get_optimistic_rounding
from src.constants import TemporalResolution

def test_get_optimistic_rounding_daily():
    """
    Test rounding for daily temporal resolution.
    """
    start = datetime(2023, 11, 15, 10, 30, tzinfo=timezone.utc)
    end = datetime(2023, 11, 15, 23, 45, tzinfo=timezone.utc)
    
    rounded_start, rounded_end = get_optimistic_rounding(start, end, TemporalResolution.DAILY)
    
    # Expected results
    assert rounded_start == datetime(2023, 11, 15, 0, 0, 0, 0, tzinfo=timezone.utc)
    assert rounded_end == datetime(2023, 11, 15, 23, 59, 59, 999999, tzinfo=timezone.utc)

def test_get_optimistic_rounding_monthly():
    """
    Test rounding for monthly temporal resolution.
    """
    start = datetime(2023, 11, 15, 10, 30, tzinfo=timezone.utc)
    end = datetime(2023, 11, 20, 23, 45, tzinfo=timezone.utc)

    rounded_start, rounded_end = get_optimistic_rounding(start, end, TemporalResolution.MONTHLY)
    
    # Expected results
    assert rounded_start == datetime(2023, 11, 1, 0, 0, 0, 0, tzinfo=timezone.utc)  # First day of the month
    assert rounded_end == datetime(2023, 11, 30, 23, 59, 59, 999999, tzinfo=timezone.utc)  # Last day of the month

def test_get_optimistic_rounding_unsupported():
    """
    Test behavior when unsupported temporal resolution is provided.
    """
    start = datetime(2023, 11, 15, 10, 30, tzinfo=timezone.utc)
    end = datetime(2023, 11, 20, 23, 45, tzinfo=timezone.utc)
    
    with pytest.raises(ValueError, match="Temporal resolution .* not supported."):
        get_optimistic_rounding(start, end, "YEARLY")  # Invalid resolution
