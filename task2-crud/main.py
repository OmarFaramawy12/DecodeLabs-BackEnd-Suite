# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas, crud
from database import engine, get_db
'''
── Create all tables on startup ──
1- SQLAlchemy reads your models.py
2- creates the actual tables in the .db file if they don't exist

'''
 
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DecodeLabs API — Project 2",
    description="Database Integration: Full CRUD with SQLite + SQLAlchemy",
    version="2.0.0"
)


# Step-1: Checking if the API is running
@app.get("/")
def root():
    return {"status": "ok", "project": "Database CRUD — Project 2"}


# Step-2: CREATE user — POST /users → 201 Created
@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Checking for duplicate email before inserting
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=409,   # 409 Conflict: appropriate status code for duplicate entries
            detail=f"Email '{user.email}' is already registered"
        )

    if crud.get_user_by_username(db, user.username.strip()):
        raise HTTPException(
            status_code=409,
            detail=f"Username '{user.username.strip()}' is already taken"
        )

    result = crud.create_user(db, user)
    if result is None:
        raise HTTPException(
            status_code=409,
            detail="A duplicate entry was detected"
        )
    return result



# Step-3: READ all users — GET /users → 200 OK

@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_users(db, skip=skip, limit=limit)


# Step-4: READ single user — GET /users/{id} → 200 OK
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Step-5: UPDATE user — PATCH /users/{id} → 200 OK (partial update: only send what changed)
@app.patch("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, updates: schemas.UserUpdate, db: Session = Depends(get_db)):
    try:
        user = crud.update_user(db, user_id, updates)
    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Username or email is already in use"
        )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Step-6: DELETE user — DELETE /users/{id} → 204 No Content
# 204 means success but nothing to return (Empty response body)
@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")