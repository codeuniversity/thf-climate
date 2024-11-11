from fastapi import APIRouter, Depends
from . import schemas, service

router = APIRouter()

@router.get("/index", response_model=schemas.WeatherDataResponse)
async def get_weather_data(request: schemas.WeatherDataRequest = Depends()):
    return await service.fetch_weather_data(request)

