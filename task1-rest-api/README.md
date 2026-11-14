# Project 1: REST API Fundamentals
Powered by DecodeLabs | Batch 2026

## Tech Stack
- FastAPI
- Pydantic Validation
- Uvicorn Server

## Setup
1. Activate venv:
   source venv/Scripts/activate

2. Install dependencies:
   pip install -r requirements.txt

3. Run the server:
   uvicorn main:app --reload

4. Open interactive docs:
   http://127.0.0.1:8000/docs

## API Endpoints
| Method | Endpoint         | Description        | Status |
|--------|------------------|--------------------|--------|
| GET    | /                | Health check       | 200    |
| GET    | /products        | Get all products   | 200    |
| GET    | /products/{id}   | Get single product | 200    |
| POST   | /products        | Create product     | 201    |

## Key Concepts Learned
- REST API fundamentals
- HTTP methods (GET, POST)
- JSON request/response
- Path parameters
- Pydantic data validation
- Stateless architecture