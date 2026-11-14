# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from security import hash_password, verify_password
from auth import create_access_token
from dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DecodeLabs API — Project 3",
    description="Secure Authentication System with Argon2id + JWT",
    version="3.0.0"
)



# Step-1: Checking Server Health
@app.get("/")
def root():
    return {"status": "ok", "project": "Secure Auth — Project 3"}



# Step-2: User Registration - POST /auth/register
# The Front Door: hash password, store user

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(user_data: UserRegister, db: Session = Depends(get_db)):

    # Check duplicate email
    if db.query(models.User).filter(
        models.User.email == user_data.email
    ).first():
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    # Check duplicate username
    if db.query(models.User).filter(
        models.User.username == user_data.username
    ).first():
        raise HTTPException(
            status_code=409,
            detail="Username already taken"
        )

    
    # Plain password goes INTO the grinder
    # Hash comes OUT — plain password is discarded forever
    hashed = hash_password(user_data.password)

    new_user = models.User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed    # Store ONLY the hash
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# Step-3: User Login - POST /auth/login
# Verify password → Issue JWT Wristband

@app.post("/auth/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2 form sends "username" field — we use it as email
    user = db.query(models.User).filter(
        models.User.email == form_data.username  # username field = email
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}



# Step-4: Get User Profile (PROTECTED ROUTE) - GET /auth/me
# Requires valid JWT — The Bouncer runs first
# Depends(get_current_user) = The Bouncer checkpoint
@app.get("/auth/me", response_model=UserResponse)
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    # If we reach this line, the Bouncer already verified the token
    # current_user is the authenticated user from the DB
    return current_user


# Step-5: Access User Dashboard (PROTECTED ROUTE) - GET /auth/dashboard
@app.get("/auth/dashboard")
def dashboard(current_user: models.User = Depends(get_current_user)):
    return {
        "message": f"Welcome to your dashboard, {current_user.username}!",
        "user_id": current_user.id,
        "email": current_user.email
    }