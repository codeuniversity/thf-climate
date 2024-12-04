from fastapi import APIRouter, Depends
from . import schemas, service
import os

router = APIRouter()

@router.get("/index", response_model=schemas.WeatherDataResponse)
async def get_weather_data(request: schemas.WeatherDataRequest = Depends()):
    return await service.fetch_weather_data(request)

@router.get("/test-env")
async def testenv():
    return os.getenv("GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_CREDENTIALS")

