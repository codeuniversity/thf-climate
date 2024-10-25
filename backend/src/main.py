from fastapi import FastAPI

from src.routes.temp import weather_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(weather_router, prefix="/weather", tags=["Temperature Data"])
