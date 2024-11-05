from pydantic import BaseModel
import requests
from .utils import LocationLatLong
from datetime import datetime

class WeatherData(BaseModel):

    @staticmethod
    def get(climaticVariable, startDate, endDate, location):

        # format inputs
        start_date = datetime.fromtimestamp(startDate).strftime("%Y-%m-%d")
        end_date = datetime.fromtimestamp(endDate).strftime("%Y-%m-%d")
        coordinates = LocationLatLong[location].value

        # get the data from open-meteo api
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": coordinates[0],
            "longitude": coordinates[1],
            "start_date": start_date,
            "end_date": end_date,
            "hourly": climaticVariable
        }

        response = requests.get(url, params=params)
        return response.json()