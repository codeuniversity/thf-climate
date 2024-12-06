import os
from enum import Enum

from ..constants import IndexType
from ..cache import ndvi_cache
from ..cache import msavi_cache


TIMESTAMP = "timestamp"
CACHE_PATH = "../cache/"


class ChosenCache(Enum):
    NDVI = ndvi_cache.ndvi_daily_cache
    MSAVI = msavi_cache.msavi_daily_cache


index_type_to_cache = {
    IndexType.NDVI: ChosenCache.NDVI,
    IndexType.MSAVI: ChosenCache.MSAVI,
}


class CacheName(Enum):
    NDVI = "ndvi_daily_cache"
    MSAVI = "msavi_daily_cache"


index_type_to_cache_name = {
    IndexType.NDVI: CacheName.NDVI,
    IndexType.MSAVI: CacheName.MSAVI,
}


class CacheFileName(Enum):
    NDVI = "ndvi_cache.py"
    MSAVI = "msavi_cache.py"


index_type_to_cache_file = {
    IndexType.NDVI: CacheFileName.NDVI,
    IndexType.MSAVI: CacheFileName.MSAVI,
}


def load_cache_file(index_type):
    try:
        cache_list = index_type_to_cache[index_type].value
        if isinstance(cache_list, list) and all(
            isinstance(item, dict) for item in cache_list
        ):
            return cache_list
    except (SyntaxError, ValueError, IndexError):
        pass

    return []


def save_cache_to_file(cache, index_type):
    """Save the updated cache to the file, maintaining the variable structure."""
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(
        dirname, CACHE_PATH, index_type_to_cache_file[index_type].value
    )
    with open(filepath, "w") as file:
        cache_name = index_type_to_cache_name[index_type].value
        file.write(f"{cache_name} = [\n")
        for entry in cache:
            file.write(f"    {entry},\n")
        file.write("]\n")


def update_cache_file(data, index_type: IndexType):
    """Update the cache with new data while maintaining chronological order."""
    cache = load_cache_file(index_type)
    existing_timestamps = {entry[TIMESTAMP] for entry in cache}

    # Add only new entries
    new_entries = [
        entry for entry in data if entry[TIMESTAMP] not in existing_timestamps
    ]
    cache.extend(new_entries)

    # Sort the cache by timestamp
    cache.sort(key=lambda x: x[TIMESTAMP])

    # Save back to the file
    save_cache_to_file(cache, index_type)


def update_cache(input: list[dict], index_type: IndexType):
    try:
        if isinstance(input, list) and all(isinstance(item, dict) for item in input):
            update_cache_file(input, index_type)
            print("Cache updated successfully.")
        else:
            print("Invalid input format. Expected a list of dictionaries.")
    except ValueError as e:
        print(f"Error parsing input data: {e}")
