# schemas.py
# The Translator's output shapes
# Raw API gives 100+ fields — we return only what matters

from pydantic import BaseModel
from typing import Optional


# CURRENT WEATHER — clean simple response
class CurrentWeather(BaseModel):
    city: str
    latitude: float
    longitude: float
    temperature_celsius: float
    windspeed_kmh: float
    weather_description: str


# HOURLY FORECAST ITEM — one hour's data
class HourlyForecastItem(BaseModel):
    time: str
    temperature_celsius: float
    precipitation_mm: float


# FULL FORECAST RESPONSE
class WeatherForecast(BaseModel):
    city: str
    latitude: float
    longitude: float
    hourly_forecast: list[HourlyForecastItem]


# ERROR RESPONSE — clean error for clients
class WeatherError(BaseModel):
    error: str
    detail: Optional[str] = None