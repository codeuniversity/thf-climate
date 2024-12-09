from pydantic import BaseModel
from abc import ABC, abstractmethod
import requests
from .utils import LocationLatLong, get_matching_json_file
from datetime import datetime
from ..constants import TemporalResolution
from calendar import monthrange

class WeatherDataProvider(ABC):
    @abstractmethod
    def fetch_data(self, weatherVariable, temporalResolution, startDate, endDate, location):
        pass

# Weather data class for getting the weather data from open meteo api
class WeatherDataOpenMeteo(WeatherDataProvider):

    def fetch_data(self, weatherVariable, temporalResolution, startDate, endDate, location):

        # format inputs
        if temporalResolution == TemporalResolution.DAILY:
            start_date = datetime.fromtimestamp(startDate).strftime("%Y-%m-%d")
            end_date = datetime.fromtimestamp(endDate).strftime("%Y-%m-%d")
        elif temporalResolution == TemporalResolution.MONTHLY:
            start_date = datetime.fromtimestamp(startDate).replace(day=1).strftime("%Y-%m-%d")
            dt = datetime.fromtimestamp(endDate)
            last_day = monthrange(dt.year, dt.month)[1]
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = min(dt.replace(day=last_day), today).strftime("%Y-%m-%d")
        coordinates = LocationLatLong[location].value

        # get the data from open-meteo api
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": coordinates[0],
            "longitude": coordinates[1],
            "start_date": start_date,
            "end_date": end_date,
            "hourly": weatherVariable
        }

        response = requests.get(url, params=params)
        return response.json()


# Weather data class for getting the weather data from cached files
class WeatherDataCached(WeatherDataProvider):

    # get data
    def fetch_data(self, weatherVariable, temporalResolution, startDate, endDate, location):

        # get cached data
        data = get_matching_json_file('src/weather/cached_data', startDate, endDate, weatherVariable.value)

        # change the provider to open meteo if there is no cached data
        if data == None:
            provider = WeatherDataOpenMeteo()
            return provider.fetch_data(weatherVariable, temporalResolution, startDate, endDate, location)

        return self.filter_data(data, weatherVariable, temporalResolution, startDate, endDate)

    # filter the cached data
    def filter_data(self, data, weatherVariable, temporalResolution, startDate, endDate):

        # format date
        if temporalResolution == TemporalResolution.DAILY:
            start_date = datetime.fromtimestamp(startDate)
            end_date = datetime.fromtimestamp(endDate)
        elif temporalResolution == TemporalResolution.MONTHLY:
            start_date = datetime.fromtimestamp(startDate).replace(day=1)
            dt = datetime.fromtimestamp(endDate)
            last_day = monthrange(dt.year, dt.month)[1]
            end_date = dt.replace(day=last_day)

        # format data
        time_data = data["hourly"]["time"]
        weather_data = data["hourly"][weatherVariable.value]
        filtered_data = filter(
            lambda item: start_date <= datetime.strptime(item[0], "%Y-%m-%dT%H:%M") <= end_date,
            zip(time_data, weather_data),
        )
        filtered_time, filtered_weather = zip(*filtered_data)
        data["hourly"]["time"] = list(filtered_time)
        data["hourly"][weatherVariable.value] = list(filtered_weather)

        return data
