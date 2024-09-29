import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import ee

from thf_climate import config


def authenticate():
    ee.Authenticate()
    ee.Initialize(project=config.GOOGLE_PROJECT_ID)
    print(ee.String("Hello from the Earth Engine servers!").getInfo())


authenticate()
