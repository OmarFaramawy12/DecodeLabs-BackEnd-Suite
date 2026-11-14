# DecodeLabs Backend Suite

Four backend milestones built with Python and FastAPI during the DecodeLabs
Backend Development track (Batch 2026). Each milestone adds one layer, and
each lives in its own folder with its own `requirements.txt`, `.env.example`
and README. They are **separate apps, not one combined service** (yet).

| Folder | Milestone | What it demonstrates |
|---|---|---|
| `task1-rest-api/` | REST API fundamentals | GET/POST routes, Pydantic validation, JSON responses, 404/201 status codes (in-memory data) |
| `task2-crud/` | Database integration | SQLAlchemy + SQLite `User` table, full CRUD, partial update (PATCH), duplicate email/username → 409 |
| `task3-auth/` | Secure authentication | Argon2id password hashing, JWT login with 30-min expiry, protected routes via a FastAPI dependency |
| `task4-weather-api/` | Third-party API integration | Async httpx client for Open-Meteo, response reshaping, timeout/network error handling |

## Run any task

```bash
cd task2-crud                     # or task1-rest-api, task3-auth, task4-weather-api
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # tasks 2-4 only; edit values (task 3: set JWT_SECRET_KEY)
uvicorn main:app --reload         # interactive docs at http://127.0.0.1:8000/docs
```

## Known limitations

- No automated tests are included in the repo.
- Task 4 uses Open-Meteo, which needs no API key, so key storage is not exercised.
  It supports 10 hard-coded cities, with no geocoding or caching.
- Tasks 2 and 3 each define their own `User` model; they are not merged.
- SQLite only; no migrations.
