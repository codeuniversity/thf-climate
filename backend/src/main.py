from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.temp import weather_router

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


app.include_router(weather_router, prefix="/weather", tags=["Temperature Data"])
