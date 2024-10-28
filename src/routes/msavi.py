from fastapi import APIRouter, Query

from src.constants import LocationName

msavi_router = APIRouter()

@msavi_router.get('/msavi')
def get_msavi(
    startDate: int = Query(..., description="Beginning of requested date range in UNIX timestamp as seconds"),
    endDate: int = Query(..., description="End of requested date range in UNIX timestamp as seconds"),
    location: LocationName = Query(..., description="Name of the requested location")
):
    return {
        "meta": {
            "index": "MSAVI",
            "location": LocationName[location].value,
            "startDate": startDate,
            "endDate": endDate,

        }
    }
