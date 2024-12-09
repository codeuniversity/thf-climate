from fastapi import HTTPException
import time


# Timestamp
def validate_timestamp_in_range(timestamp):
    min_timestamp = 1388530801  # 01/01/2014
    max_timestamp = 2208985201  # 01/01/2040
    if not (min_timestamp <= timestamp <= max_timestamp):
        raise HTTPException(
            status_code=400, detail=f"Timestamp must be between {min_timestamp} and {max_timestamp}")
    return timestamp


def validate_timestamp_in_range_of_S2_imagery(start_timestamp, end_timestamp):
    min_timestamp = 1491004800  # 01/04/2017
    max_timestamp = int(time.time())  # Current timestamp
    if not (min_timestamp <= start_timestamp <= max_timestamp and min_timestamp <= end_timestamp <= max_timestamp):
        raise HTTPException(
            status_code=400, detail=f"Timestamp must be between {min_timestamp} and now ({max_timestamp})")
    return


def validate_timestamp_start_date_before_end_date(startDate, endDate):
    if endDate <= startDate:
        raise HTTPException(
            status_code=400, detail="endDate must be after startDate")
    return endDate
