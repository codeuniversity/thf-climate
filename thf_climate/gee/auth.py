import base64
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import ee

from thf_climate import config
from thf_climate.config import Environment


def authenticate():
    if config.ENVIRONMENT == Environment.LOCAL.value:
        ee.Authenticate()
        ee.Initialize(project=config.GOOGLE_PROJECT_ID)
        print("Successfully authenticated - LOCAL Environment")
    elif (
        config.ENVIRONMENT == Environment.DEVELOPMENT.value
        or config.ENVIRONMENT == Environment.PRODUCTION.value
    ):
        service_account = config.GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_EMAIL
        credentials = ee.ServiceAccountCredentials(
            service_account,
            key_data=base64.b64decode(
                config.GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_CREDENTIALS_B64
            ).decode("utf-8"),
        )
        ee.Initialize(credentials)
        print("Successfully authenticated - DEVELOPMENT/PRODUCTION Environment")
    else:
        raise ValueError("Invalid environment:" + config.ENVIRONMENT)


authenticate()
