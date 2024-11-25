import os
import requests


def test_api_response():
    # url = os.getenv("API_URL")#"https://thf-climate-run-1020174331409.europe-west3.run.app"

    # Make a GET request to the API
    response = requests.get(os.getenv("API_BASE_URL"))

    # Verify the response status code
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Verify the response body
    expected_response = {"Hello": "World"}
    assert response.json() == expected_response, f"Expected {expected_response}, got {response.json()}"
