from fastapi import FastAPI

from .weather.router import router as weather_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(weather_router, prefix="/weather", tags=["Temperature Data"])
