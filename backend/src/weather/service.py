from collections import defaultdict
from datetime import datetime
from .schemas import WeatherDataResponse, WeatherDataMeta, DataPoint, WeatherVariableUnit
from .models import WeatherDataCached
from ..constants import TemporalResolution, AggregationMethod
from statistics import mean, median


async def fetch_weather_data(request) -> WeatherDataResponse:
    # get and format the data
    data_provider = WeatherDataCached()
    data = data_provider.fetch_data(request.weatherVariable, request.temporalResolution, request.startDate, request.endDate, request.location)
    formated_data = await format_weather_data(data, request.weatherVariable, request.temporalResolution, request.aggregation)

    return WeatherDataResponse(
        meta=WeatherDataMeta(
            weatherVariable=request.weatherVariable,
            unit=WeatherVariableUnit[request.weatherVariable],
            location=request.location,
            startDate=request.startDate,
            endDate=request.endDate,
            temporalResolution=request.temporalResolution,
            aggregation=request.aggregation,
        ),
        data=formated_data
    )


async def format_weather_data(data, weatherVariable, temporalResolution, aggregation):
    timestamps = data["hourly"]["time"]
    values = data["hourly"][weatherVariable]

    # Dictionary to store daily values
    list_values = defaultdict(list)

    # aggregate the data on daily or monthly bases
    for timestamp, value in zip(timestamps, values):
        if temporalResolution == TemporalResolution.DAILY:
            date = datetime.fromisoformat(timestamp).date()
        elif temporalResolution == TemporalResolution.MONTHLY:
            date = datetime.fromisoformat(timestamp).strftime('%Y-%m')
            date = datetime.strptime(date + "-01", "%Y-%m-%d")
        if value != None:
            list_values[date].append(value)

    # Calculate aggregation values
    aggregation_methods = {
        AggregationMethod.MEAN: lambda temps: mean(temps),
        AggregationMethod.MEDIAN: lambda temps: median(temps),
        AggregationMethod.MAX: lambda temps: max(temps),
        AggregationMethod.MIN: lambda temps: min(temps),
    }
    list_values = {date: aggregation_methods[aggregation](temps) for date, temps in list_values.items()}

    # data_points
    data_points = list(
        map(lambda item: DataPoint(value=item[1], timestamp=item[0].strftime("%s")), list_values.items())
    )

    return data_points