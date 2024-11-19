from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, timezone

from src.constants import TemporalResolution


def get_optimistic_rounding(
    start_date: datetime, end_date: datetime, temporal_resolution: TemporalResolution
) -> (datetime, datetime):
    """Get optimistic rounding for the start date based on the temporal resolution."""

    if temporal_resolution == TemporalResolution.DAILY:
        start_date = first_second_of_day(start_date)
        end_date = last_second_of_day(end_date)
    elif temporal_resolution == TemporalResolution.MONTHLY:
        start_date = first_second_of_month(start_date)
        end_date = last_second_of_month(end_date)

    return start_date, end_date


def first_second_of_day(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def last_second_of_day(dt: datetime) -> datetime:
    return dt.replace(hour=23, minute=59, second=59, microsecond=0)


def first_second_of_month(dt: datetime) -> datetime:
    return dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def last_second_of_month(dt: datetime) -> datetime:
    next_month = dt.replace(day=1, hour=0, minute=0,
                            second=0, microsecond=0) + relativedelta(months=1)
    return (next_month - timedelta(seconds=1)).replace(tzinfo=timezone.utc)
