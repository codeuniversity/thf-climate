from fastapi import HTTPException


# Timestamp
def validate_timestamp_in_range(timestamp):
    min_timestamp = 1388530801  # 01/01/2014
    max_timestamp = 2208985201  # 01/01/2040
    if not (min_timestamp <= timestamp <= max_timestamp):
        raise HTTPException(status_code=400, detail=f"Timestamp must be between {min_timestamp} and {max_timestamp}")
    return timestamp


def validate_timestamp_startdate_before_enddate(startDate, endDate):
    if endDate <= startDate:
        raise HTTPException(status_code=400, detail="endDate must be after startDate")
    return endDate