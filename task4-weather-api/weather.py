# weather.py
# The Backend Middleman — all 4 roles in one file:
# The Vault (config via .env; Open-Meteo needs no key) + The Messenger + The Translator + The Shield

import httpx
from dotenv import load_dotenv
import os

load_dotenv()

# ── Load config from .env (The Vault) ──
BASE_URL = os.getenv("WEATHER_API_BASE_URL")
TIMEOUT  = float(os.getenv("REQUEST_TIMEOUT_SECONDS", 10))

'''
WEATHER CODE TRANSLATOR
    - Open-Meteo returns numeric weather codes (0, 1, 2...)
    - We translate them to human-readable descriptions
    - This is The Translator in action — cryptic → semantic
'''
WEATHER_CODES = {
    0:  "Clear sky",
    1:  "Mainly clear",
    2:  "Partly cloudy",
    3:  "Overcast",
    45: "Foggy",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Heavy showers",
    95: "Thunderstorm",
    99: "Thunderstorm with hail",
}


'''
CITY COORDINATES LOOKUP
    - Open-Meteo uses latitude/longitude — we map city names
    - In a real app you'd use a Geocoding API
'''
CITY_COORDINATES = {
    "london":    {"lat": 51.5074, "lon": -0.1278},
    "cairo":     {"lat": 30.0444, "lon": 31.2357},
    "new york":  {"lat": 40.7128, "lon": -74.0060},
    "paris":     {"lat": 48.8566, "lon": 2.3522},
    "dubai":     {"lat": 25.2048, "lon": 55.2708},
    "tokyo":     {"lat": 35.6762, "lon": 139.6503},
    "sydney":    {"lat": -33.8688, "lon": 151.2093},
    "berlin":    {"lat": 52.5200, "lon": 13.4050},
    "singapore": {"lat": 1.3521,  "lon": 103.8198},
    "mumbai":    {"lat": 19.0760, "lon": 72.8777},
}



# THE MESSENGER — async fetch current weather
# async/await = non-blocking I/O
async def get_current_weather(city: str) -> dict:
    """
    Fetches current weather for a city.
    Implements all 4 Middleman roles:
    - Vault: base URL/timeout from .env (no API key needed for Open-Meteo)
    - Messenger: async/await non-blocking fetch
    - Translator: raw data → clean response
    - Shield: try/except error containment
    """

    # Normalize city name
    city_lower = city.lower().strip()

    # Look up coordinates
    coords = CITY_COORDINATES.get(city_lower)
    if not coords:
        return {
            "error": "City not found",
            "detail": f"'{city}' not in supported cities: {list(CITY_COORDINATES.keys())}"
        }

    # ── THE SHIELD — wrap everything in try/except ──
    try:
        # ── THE MESSENGER — async HTTP client ──
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:

            # ── THE VAULT — config from .env ──
            # Open-Meteo needs no key; a keyed provider's key would be added here.
            response = await client.get(
                f"{BASE_URL}/forecast",
                params={
                    "latitude":        coords["lat"],
                    "longitude":       coords["lon"],
                    "current_weather": True,   # Get current conditions
                    "timezone":        "auto"  # Auto-detect timezone
                }
            )

            # Raise exception for 4xx/5xx responses
            response.raise_for_status()

            # Parse the raw JSON
            raw_data = response.json()

            # ── THE TRANSLATOR — extract only what we need ──
            # Raw response has many fields — we pick only 4
            current = raw_data["current_weather"]
            weather_code = current.get("weathercode", 0)

            # Transform cryptic fields to semantic names
            return {
                "city":                 city.title(),
                "latitude":             coords["lat"],
                "longitude":            coords["lon"],
                "temperature_celsius":  current["temperature"],
                "windspeed_kmh":        current["windspeed"],
                "weather_description":  WEATHER_CODES.get(
                                            weather_code,
                                            "Unknown conditions"
                                        )
            }

    # ── THE SHIELD — handle each error type strategically ──
    except httpx.TimeoutException:
        # Network/Timeout error → retry logic message
        return {
            "error": "Weather service timeout",
            "detail": "The weather provider took too long to respond. Please try again."
        }

    except httpx.HTTPStatusError as e:
        # 4xx/5xx error from weather API
        return {
            "error": f"Weather service error {e.response.status_code}",
            "detail": "The weather provider returned an error"
        }

    except httpx.RequestError:
        # Network connection error
        return {
            "error": "Network connection failed",
            "detail": "Could not reach the weather service. Check your connection."
        }

    except Exception as e:
        # Catch-all — never let external failures crash our server
        return {
            "error": "Unexpected error",
            "detail": "An internal error occurred while fetching weather data"
        }


# HOURLY FORECAST — next 24 hours
async def get_hourly_forecast(city: str) -> dict:
    """
    Fetches 24-hour forecast for a city.
    Demonstrates The Translator with list transformation:
    Raw hourly data (100+ entries) → filtered 24 clean items
    """

    city_lower = city.lower().strip()
    coords = CITY_COORDINATES.get(city_lower)

    if not coords:
        return {
            "error": "City not found",
            "detail": f"'{city}' not supported"
        }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(
                f"{BASE_URL}/forecast",
                params={
                    "latitude":              coords["lat"],
                    "longitude":             coords["lon"],
                    "hourly":                "temperature_2m,precipitation",
                    "forecast_days":         1,       # Today only
                    "timezone":              "auto"
                }
            )
            response.raise_for_status()
            raw_data = response.json()

            # ── THE TRANSLATOR pipeline ──
            # Raw: two separate arrays (times[], temps[], precip[])
            # Clean: list of unified hourly objects
            hourly = raw_data["hourly"]
            times  = hourly["time"]
            temps  = hourly["temperature_2m"]
            precip = hourly["precipitation"]

            # Zip arrays together and take first 24 hours
            # This is the .map() pattern from your slides
            forecast = [
                {
                    "time":                time,
                    "temperature_celsius": temp,
                    "precipitation_mm":    rain
                }
                for time, temp, rain in zip(times, temps, precip)
            ][:24]  # Limit to 24 hours

            return {
                "city":             city.title(),
                "latitude":         coords["lat"],
                "longitude":        coords["lon"],
                "hourly_forecast":  forecast
            }

    except httpx.TimeoutException:
        return {"error": "Timeout", "detail": "Weather service timed out"}
    except httpx.HTTPStatusError as e:
        return {"error": f"API Error {e.response.status_code}", "detail": str(e)}
    except Exception:
        return {"error": "Unexpected error", "detail": "Failed to fetch forecast"}