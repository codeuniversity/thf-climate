from fastapi import HTTPException


# Timestamp
def validate_timestamp_in_range(timestamp):
    min_timestamp = 1388530801  # 01/01/2014
    max_timestamp = 2208985201  # 01/01/2040
    if not (min_timestamp <= timestamp <= max_timestamp):
        raise ValueError(
            f"Timestamp must be between {min_timestamp} and {max_timestamp}"
        )


def validate_timestamp_start_date_before_end_date(startDate, endDate):
    if endDate <= startDate:
        raise HTTPException(status_code=400, detail="endDate must be after startDate")
