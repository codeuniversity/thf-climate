from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.ndvi import ndvi_router

from .weather.router import router as weather_router

app = FastAPI()

origins = ["http://localhost:5173"]

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
app.include_router(ndvi_router, prefix="/index", tags=["NDVI Data"])