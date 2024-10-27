from .schemas import TemperatureDataResponse, TemperatureDataMeta, DataPoint

async def fetch_temperature_data(request):
    # Simulate data fetching or processing
    sample_response = TemperatureDataResponse(
        meta=TemperatureDataMeta(
            unit="Celsius",
            location=request.location,
            startDate=request.startDate,
            endDate=request.endDate,
            temporalResolution=request.temporalResolution,
            aggregation=request.aggregation,
        ),
        data=[
            DataPoint(value=13.45, timestamp=1617321600),
            DataPoint(value=15.5, timestamp=1617555600),
            DataPoint(value=24.0, timestamp=1677721600),
        ],
    )
    return sample_response