from collections import defaultdict
from datetime import datetime
from .schemas import TemperatureDataResponse, TemperatureDataMeta, DataPoint
from .models import TemperatureData
from ..constants import TemporalResolution, AggregationMethod
from statistics import mean, median


async def fetch_temperature_data(request):
    # get and format the data
    data = TemperatureData.get(request.startDate, request.endDate, request.location)
    formated_data = await format_temperature_data(data, request.temporalResolution, request.aggregation)

    return TemperatureDataResponse(
        meta=TemperatureDataMeta(
            unit="Celsius",
            location=request.location,
            startDate=request.startDate,
            endDate=request.endDate,
            temporalResolution=request.temporalResolution,
            aggregation=request.aggregation,
        ),
        data=formated_data
    )


async def format_temperature_data(data, temporalResolution, aggregation):
    timestamps = data["hourly"]["time"]
    temperatures = data["hourly"]["temperature_2m"]

    # Dictionary to store daily temperatures
    list_temperatures = defaultdict(list)

    # aggregate the data on daily or monthly bases
    for timestamp, temperature in zip(timestamps, temperatures):
        if temporalResolution == TemporalResolution.DAILY:
            date = datetime.fromisoformat(timestamp).date()
        elif temporalResolution == TemporalResolution.MONTHLY:
            date = datetime.fromisoformat(timestamp).strftime('%Y-%m')
            date = datetime.strptime(date + "-01", "%Y-%m-%d")
        list_temperatures[date].append(temperature)

    # Calculate aggregation temperatures
    if aggregation == AggregationMethod.MEAN:
        list_temperatures = {date: mean(temps) for date, temps in list_temperatures.items()}
    elif aggregation == AggregationMethod.MEDIAN:
        list_temperatures = {date: median(temps) for date, temps in list_temperatures.items()}
    elif aggregation == AggregationMethod.MAX:
        list_temperatures = {date: max(temps) for date, temps in list_temperatures.items()}
    elif aggregation == AggregationMethod.MIN:
        list_temperatures = {date: min(temps) for date, temps in list_temperatures.items()}

    # data_points
    data_points = []
    for date, temp in list_temperatures.items():
        timestamp = date.strftime("%s")
        data_points.append(DataPoint(value=temp, timestamp=timestamp))

    return data_points