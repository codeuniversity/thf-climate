import os
import pytest

@pytest.fixture
def base_url():
    """
    Fixture to provide the base URL dynamically based on environment variables.
    """
    return os.getenv("BASE_URL", "https://thf-climate-run-1020174331409.europe-west3.run.app")  # Default to local development server
