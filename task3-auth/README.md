# Project 3: Secure Authentication System
Powered by DecodeLabs | Batch 2026

## Tech Stack
- FastAPI + SQLAlchemy + SQLite
- Argon2id password hashing (OWASP recommended)
- JWT stateless authentication (python-jose)

## Setup
1. source venv/Scripts/activate
2. pip install -r requirements.txt
3. Create .env:
   DATABASE_URL=sqlite:///./project3_auth.db
   JWT_SECRET_KEY=your_secret_key_here
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_MINUTES=30
4. uvicorn main:app --reload

## API Endpoints
| Method | Endpoint         | Auth Required | Description      |
|--------|-----------------|---------------|------------------|
| POST   | /auth/register  | No            | Create account   |
| POST   | /auth/login     | No            | Get JWT token    |
| GET    | /auth/me        | Yes ✅        | Your profile     |
| GET    | /auth/dashboard | Yes ✅        | Your dashboard   |

## Security Features
- Argon2id hashing (64MB memory cost, 3 iterations)
- JWT tokens with 30 minute expiry
- 401 bouncer middleware on protected routes
- Secrets managed via .env + .gitignore