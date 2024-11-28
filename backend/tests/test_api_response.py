import os
import requests
from dotenv import load_dotenv

   # Load environment variables from .env file
load_dotenv()

def test_api_response():
       # Make a GET request to the API
       api_base_url = os.getenv("API_BASE_URL")
       assert api_base_url is not None, "API_BASE_URL is not set"

       response = requests.get(api_base_url)

       # Verify the response status code
       assert response.status_code == 200, f"Expected 200, got {response.status_code}"

       # Verify the response body
       expected_response = {"Hello": "World"}
       assert response.json() == expected_response, f"Expected {expected_response}, got {response.json()}"