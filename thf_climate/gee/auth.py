import ee

from thf_climate import config


def authenticate():
    ee.Authenticate()
    ee.Initialize(project=config.GOOGLE_PROJECT_ID)
    print(ee.String("Hello from the Earth Engine servers!").getInfo())
