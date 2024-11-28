import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_weather_valid_input():
    api_base_url = os.getenv("API_BASE_URL")
    assert api_base_url, "API_BASE_URL is not set"

    params = {
        "weatherVariable": "temperature_2m",
        "startDate": 1448526528,
        "endDate": 1700987328,
        "location": "TEMPELHOFER_FELD",  # Valid location
        "temporalResolution": "DAILY",  # Valid resolution
        "aggregation": "MEAN",  # Valid method
    }
    response = requests.get(f"{api_base_url}/weather/index", params=params)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "value" in data["data"][0]

def test_weather_invalid_location():
    api_base_url = os.getenv("API_BASE_URL")
    assert api_base_url, "API_BASE_URL is not set"

    params = {
        "weatherVariable": "temperature_2m",
        "startDate": 1448526528,
        "endDate": 1700987328,
        "location": "UNKNOWN_LOCATION",  # Invalid location
        "temporalResolution": "DAILY",
        "aggregation": "MEAN",
    }
    response = requests.get(f"{api_base_url}/weather/index", params=params)
    
    assert response.status_code == 422, f"Expected 422, got {response.status_code}"  # Adjusted expectation