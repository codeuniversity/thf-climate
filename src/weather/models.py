from pydantic import BaseModel
import requests
from .utils import LocationLatLong
from datetime import datetime
from ..constants import TemporalResolution
from calendar import monthrange

class WeatherData(BaseModel):

    @staticmethod
    def get(climaticVariable, temporalResolution, startDate, endDate, location):

        # format inputs
        if temporalResolution == TemporalResolution.DAILY:
            start_date = datetime.fromtimestamp(startDate).strftime("%Y-%m-%d")
            end_date = datetime.fromtimestamp(endDate).strftime("%Y-%m-%d")
        elif temporalResolution == TemporalResolution.MONTHLY:
            start_date = datetime.fromtimestamp(startDate).replace(day=1).strftime("%Y-%m-%d")
            dt = datetime.fromtimestamp(endDate)
            last_day = monthrange(dt.year, dt.month)[1]
            end_date = dt.replace(day=last_day).strftime("%Y-%m-%d")
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