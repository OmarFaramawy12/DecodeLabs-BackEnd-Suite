# Project 2: Database Integration (CRUD)

## Setup
1. Create and activate venv
2. pip install -r requirements.txt
3. Create .env with DATABASE_URL=sqlite:///./decodelabs.db
4. uvicorn main:app --reload

## Endpoints
- POST   /users       → Create user (201)
- GET    /users       → List all users (200)
- GET    /users/{id}  → Get single user (200)
- PATCH  /users/{id}  → Update user (200)
- DELETE /users/{id}  → Delete user (204)

Duplicate email or username → 409 Conflict (on create and on update).