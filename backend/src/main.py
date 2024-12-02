from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.sat_index_router import sat_index_router

from .weather.router import router as weather_router

app = FastAPI()

origins = ["http://localhost:5173", "https://thf-climate-frontend-run-1020174331409.europe-west3.run.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(weather_router, prefix="/weather", tags=["Weather Data"])
app.include_router(sat_index_router, prefix="/index", tags=["Vegetation Indices"])
