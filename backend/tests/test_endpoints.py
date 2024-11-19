import httpx
import pytest

BASE_URL = "https://thf-climate-run-1020174331409.europe-west3.run.app/weather/index"

@pytest.mark.asyncio
async def test_weather_temperature_json_format():
    """
    Test that the `/weather/index` endpoint returns JSON in the correct format.
    """
    valid_params = {
        "weatherVariable": "temperature_2m",
        "startDate": 1388530801,
        "endDate": 1391209201,
        "location": "TEMPELHOFER_FELD",
        "temporalResolution": "DAILY",
        "aggregation": "MEAN"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=valid_params)

        # Assert the response is successful
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        # Parse the JSON response
        data = response.json()

        # Validate the structure of the response
        assert "data" in data, "'data' key is missing in the response"
        assert isinstance(data["data"], list), "'data' should be a list"
        if data["data"]:  # Check if there are entries in the data
            assert "timestamp" in data["data"][0], "'timestamp' key missing in data entries"
            assert "value" in data["data"][0], "'value' key missing in data entries"


@pytest.mark.asyncio
async def test_weather_index_invalid_inputs():
    """
    Test that the `/weather/index` endpoint rejects invalid inputs.
    """
    invalid_params = {
        "weatherVariable": "invalid_variable", 
        "startDate": "invalid_date", 
        "endDate": "invalid_date",
        "location": "INVALID_LOCATION",  
        "temporalResolution": "INVALID",  
        "aggregation": "INVALID"  
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=invalid_params)

        # Assert that the response indicates a client error
        assert response.status_code == 400 or response.status_code == 422, (
            f"Unexpected status code for invalid input: {response.status_code}"
        )

        # Parse the error response (optional, if the API provides error details)
        error_data = response.json()
        assert "detail" in error_data, "'detail' key missing in error response"
        assert isinstance(error_data["detail"], list) or isinstance(error_data["detail"], str), (
            "'detail' should be a list or string in the error response"
        )
