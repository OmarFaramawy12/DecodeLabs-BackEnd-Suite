'''
This module handles 
    a- user authentication, 
    b- including registration, login, and JWT token management.

1- Creates and verifies JWT tokens
2- JWT structure: Header.Payload.Signature
3- Only the server with the SECRET KEY can create valid signatures

'''

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

#Step-1: Load environment variables from .env file
load_dotenv()

# Step-2: Get JWT configuration from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")  
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 30))

# STEP-3: Function to create a JWT token (Acess Token)
def create_access_token(data: dict) -> str:
    """
    Creates a signed JWT token.
    'data' contains the payload — what we embed in the token.
    We always add an expiry time (exp) so tokens don't live forever.
    """
    payload = data.copy()

    # Token expires after EXPIRE_MINUTES from now
    expiry = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    payload.update({"exp": expiry})

    # Sign: Hash(Header + Payload + SECRET_KEY) = Signature
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# Step-4: Function to verify a JWT token
def verify_access_token(token: str) -> dict | None:
    """
    Verifies a JWT token:
    1. Checks the signature hasn't been tampered with
    2. Checks it hasn't expired
    Returns the payload dict if valid, None if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None