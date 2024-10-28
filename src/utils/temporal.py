from datetime import datetime, timedelta

from src.constants import TemporalResolution


def get_optimistic_rounding(
    start_date: datetime, end_date: datetime, temporal_resolution: TemporalResolution
) -> (datetime, datetime):
    """Get optimistic rounding for the start date based on the temporal resolution."""
    if temporal_resolution == TemporalResolution.DAILY:
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif temporal_resolution == TemporalResolution.MONTHLY:
        start_date = start_date.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        end_date = last_time_of_month(end_date)
        # Set end_date to the last day of the month at 23:59:59.999999
        next_month = end_date.replace(day=1, month=end_date.month % 12 + 1)
        end_date = next_month - timedelta(seconds=1)
    else:
        raise ValueError(f"Temporal resolution {temporal_resolution} not supported.")
    return start_date, end_date


def last_time_of_month(dt: datetime) -> datetime:
    # Move to the beginning of the next month
    if dt.month == 12:
        next_month = datetime(dt.year + 1, 1, 1)
    else:
        next_month = datetime(dt.year, dt.month + 1, 1)

    # Subtract one microsecond to get the last moment of the given month
    last_time = next_month - timedelta(microseconds=1)

    return last_time
