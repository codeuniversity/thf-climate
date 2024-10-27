from fastapi import APIRouter, Depends
from . import schemas, service

router = APIRouter()

@router.get("/temperature", response_model=schemas.TemperatureDataResponse)
async def get_temperature_data(request: schemas.TemperatureDataRequest = Depends()):
    return await service.fetch_temperature_data(request)

