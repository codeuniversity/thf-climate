from fastapi import FastAPI

from src.routes.msavi import msavi_router
from src.routes.ndvi import ndvi_router
from src.routes.temp import weather_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(weather_router, prefix="/weather", tags=["Temperature Data"])
app.include_router(ndvi_router, prefix="/index", tags=["NDVI Data"])
app.include_router(msavi_router, prefix="/index", tags=["MSAVI Data"])
