import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ndvi_valid_input():
    api_base_url = os.getenv("API_BASE_URL")
    # assert api_base_url, "API_BASE_URL is not set"

    params = {
        "startDate": 1448526528,  
        "endDate": 1700987328,   
        "location": "TEMPELHOFER_FELD",
        "temporalResolution": "DAILY",
        "aggregation": "MEAN",
    }
    response = requests.get(f"{api_base_url}/index/ndvi", params=params)
    
    assert response.status_code == 200, f"Expected 200, got {response.json()}"
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0
    assert "value" in data["data"][0]

# def test_ndvi_invalid_location():
#     api_base_url = os.getenv("API_BASE_URL")
#     assert api_base_url, "API_BASE_URL is not set"

#     params = {
#         "startDate": 1448526528,
#         "endDate": 1700987328,
#         "location": "UNKNOWN_LOCATION",
#         "temporalResolution": "DAILY",
#         "aggregation": "MEAN",
#     }
#     response = requests.get(f"{api_base_url}/index/ndvi", params=params)
    
#     assert response.status_code == 422, f"Expected 422, got {response.status_code}"

# def test_ndvi_invalid_dates():
#     api_base_url = os.getenv("API_BASE_URL")
#     assert api_base_url, "API_BASE_URL is not set"

#     params = {
#         "startDate": 1700987328,  
#         "endDate": 1448526528,
#         "location": "TEMPELHOFER_FELD",
#         "temporalResolution": "DAILY",
#         "aggregation": "MEAN",
#     }
#     response = requests.get(f"{api_base_url}/index/ndvi", params=params)
    
#     assert response.status_code == 422, f"Expected 422, got {response.status_code}"