# main.py
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import weather

load_dotenv()

app = FastAPI(
    title="DecodeLabs API — Project 4",
    description="Third-Party API Integration: Weather Data Middleman",
    version="4.0.0"
)



# HEALTH CHECK
@app.get("/")
async def root():
    return {
        "status": "ok",
        "project": "Third-Party API Integration — Project 4",
        "supported_cities": [
            "London", "Cairo", "New York", "Paris",
            "Dubai", "Tokyo", "Sydney", "Berlin",
            "Singapore", "Mumbai"
        ]
    }



# CURRENT WEATHER
# GET /weather/{city}
# The complete Middleman flow for current conditions
@app.get("/weather/{city}")
async def current_weather(city: str):
    result = await weather.get_current_weather(city)

    # If result contains "error" key — something went wrong
    if "error" in result:
        raise HTTPException(
            status_code=404 if result["error"] == "City not found" else 503,
            detail=result
        )

    return {
        "status": "success",
        "source": "Open-Meteo API (via DecodeLabs Backend)",
        "data": result
    }


# 24-HOUR FORECAST
# GET /weather/{city}/forecast
@app.get("/weather/{city}/forecast")
async def hourly_forecast(city: str):
    result = await weather.get_hourly_forecast(city)

    if "error" in result:
        raise HTTPException(
            status_code=404 if result["error"] == "City not found" else 503,
            detail=result
        )

    return {
        "status": "success",
        "source": "Open-Meteo API (via DecodeLabs Backend)",
        "data": result
    }


# SUPPORTED CITIES LIST
# GET /weather/cities
@app.get("/cities")
async def get_cities():
    return {
        "status": "success",
        "supported_cities": [
            "London", "Cairo", "New York", "Paris",
            "Dubai", "Tokyo", "Sydney", "Berlin",
            "Singapore", "Mumbai"
        ]
    }