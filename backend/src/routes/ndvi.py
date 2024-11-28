from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/ndvi")
async def get_ndvi(
    startDate: int,
    endDate: int,
    location: str,
    temporalResolution: str,
    aggregation: str
):
    if startDate >= endDate:
        raise HTTPException(status_code=422, detail="Invalid date order")
    
    # Example response
    return {
        "meta": {
            "temporalResolution": temporalResolution
        },
        "data": [
            {"timestamp": startDate, "value": 0.5}
        ]
    }