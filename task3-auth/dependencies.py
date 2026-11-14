'''
This is the Middleware Checkpoint.
Every protected route passes through this FIRST.
It checks the Authorization: Bearer <token> header.
'''

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from auth import verify_access_token
import models

'''
Step-1: Define the OAuth2 scheme for extracting the token from the Authorization header
tokenUrl points to our login endpoint.
'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Step-2: Dependency function to get the current user from the token

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    THE BOUNCER — runs before every protected route.

    Exact Flow:
    1. Has token?          No  → 401 Unauthorized
    2. Signature valid?    No  → 401 Unauthorized
    3. Token expired?      Yes → 401 Unauthorized
    4. User exists in DB?  No  → 401 Unauthorized
    5. All checks pass     →   Attach user to request
    """

    # Single reusable exception — don't leak Why it failed
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Step 1 & 2: Verify token signature and expiry
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_error

    # Step 3: Extract user identity from token payload
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_error

    # Step 4: Confirm user still exists in database
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_error

    # Step 5: All checks passed — return user to the route
    return user

