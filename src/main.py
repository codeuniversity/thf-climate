from fastapi import FastAPI

from src.routes.ndvi_router import ndvi_router

from .weather.router import router as weather_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(weather_router, prefix="/weather", tags=["Temperature Data"])
app.include_router(ndvi_router, prefix="/index", tags=["NDVI Data"])
