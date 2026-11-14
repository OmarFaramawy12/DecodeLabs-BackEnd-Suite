# Project 4: Third-Party API Integration
Powered by DecodeLabs | Batch 2026

## Tech Stack
- FastAPI + httpx (async HTTP client)
- Open-Meteo Weather API (free, no key required)
- Pydantic response schemas
- python-dotenv for configuration (base URL, timeout)

## Architecture Pattern
Backend Middleman (Facade Pattern):
Frontend → FastAPI → External API
API keys stay on server, never exposed to client

## Setup
1. source venv/Scripts/activate
2. pip install -r requirements.txt
3. Create .env from .env.example
4. uvicorn main:app --reload
5. Open http://127.0.0.1:8000/docs

## API Endpoints
| Method | Endpoint                  | Description           |
|--------|---------------------------|-----------------------|
| GET    | /                         | Health check + cities |
| GET    | /cities                   | Supported cities list |
| GET    | /weather/{city}           | Current weather       |
| GET    | /weather/{city}/forecast  | 24-hour forecast      |

## Supported Cities
London, Cairo, New York, Paris, Dubai,
Tokyo, Sydney, Berlin, Singapore, Mumbai

## Key Concepts Implemented
- Async/await non-blocking HTTP requests
- Configuration via .env (Open-Meteo needs no API key; an API-key header would be injected in weather.py if a keyed provider were used)
- Data transformation (The Translator)
- Resilience error handling (The Shield)
- Graceful degradation on API failures