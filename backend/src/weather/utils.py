from enum import Enum
from fastapi import HTTPException
import time
import os
import json

class LocationLatLong(Enum):
    TEMPELHOFER_FELD = (52.4906898,13.373749)

def validate_timestamp_in_range(start, end):
    min_timestamp = -946771200  # 01/01/1940
    max_timestamp = int(time.time()) # now
    if (start < min_timestamp or end > max_timestamp):
        raise HTTPException(
            status_code=400, detail=f"Timestamp must be between {min_timestamp} and {max_timestamp}")
    elif end <= start:
        raise HTTPException(
            status_code=400, detail="endDate must be after startDate")
    return end

# Get json file from folder based on the timestamp
# matching format <start_timestamp>_<end_timestamp>_<file_name>.json
def get_matching_json_file(folder_path, timestamp_from, timestamp_to, filename):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(f'_{filename}.json'):
            try:
                # Extract start and end timestamps from the filename
                parts = file_name.split('_')
                file_start_timestamp = int(parts[0])
                file_end_timestamp = int(parts[1])

                # Check if the provided timestamps fall within the file's range
                if file_start_timestamp <= timestamp_from and file_end_timestamp >= timestamp_to:
                    file_path = os.path.join(folder_path, file_name)

                    # Load and return the JSON content
                    with open(file_path, 'r') as json_file:
                        return json.load(json_file)
            except (ValueError, IndexError, FileNotFoundError):
                continue

    return None