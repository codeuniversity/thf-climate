from collections import defaultdict
from datetime import datetime
from .schemas import WeatherDataResponse, WeatherDataMeta, DataPoint, ClimaticVariableUnit
from .models import WeatherData
from ..constants import TemporalResolution, AggregationMethod
from statistics import mean, median


async def fetch_weather_data(request):
    # get and format the data
    data = WeatherData.get(request.climaticVariable, request.temporalResolution, request.startDate, request.endDate, request.location)
    formated_data = await format_weather_data(data, request.climaticVariable, request.temporalResolution, request.aggregation)

    return WeatherDataResponse(
        meta=WeatherDataMeta(
            climaticVariable=request.climaticVariable,
            unit=ClimaticVariableUnit[request.climaticVariable],
            location=request.location,
            startDate=request.startDate,
            endDate=request.endDate,
            temporalResolution=request.temporalResolution,
            aggregation=request.aggregation,
        ),
        data=formated_data
    )


async def format_weather_data(data, climaticVariable, temporalResolution, aggregation):
    timestamps = data["hourly"]["time"]
    values = data["hourly"][climaticVariable]

    # Dictionary to store daily values
    list_values = defaultdict(list)

    # aggregate the data on daily or monthly bases
    for timestamp, value in zip(timestamps, values):
        if temporalResolution == TemporalResolution.DAILY:
            date = datetime.fromisoformat(timestamp).date()
        elif temporalResolution == TemporalResolution.MONTHLY:
            date = datetime.fromisoformat(timestamp).strftime('%Y-%m')
            date = datetime.strptime(date + "-01", "%Y-%m-%d")
        list_values[date].append(value)

    # Calculate aggregation values
    if aggregation == AggregationMethod.MEAN:
        list_values = {date: mean(temps) for date, temps in list_values.items()}
    elif aggregation == AggregationMethod.MEDIAN:
        list_values = {date: median(temps) for date, temps in list_values.items()}
    elif aggregation == AggregationMethod.MAX:
        list_values = {date: max(temps) for date, temps in list_values.items()}
    elif aggregation == AggregationMethod.MIN:
        list_values = {date: min(temps) for date, temps in list_values.items()}

    # data_points
    data_points = []
    for date, temp in list_values.items():
        timestamp = date.strftime("%s")
        data_points.append(DataPoint(value=temp, timestamp=timestamp))

    return data_points