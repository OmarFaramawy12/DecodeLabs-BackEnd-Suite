# schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


# Step-1: Registration request
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str       # Plain text — only exists here, never stored

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


# Step-2: Login request 
class UserLogin(BaseModel):
    email: EmailStr
    password: str       # Plain text — verified then discarded


# Step-3: Token response 
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Step-4: Safe user response — password_hash NEVER included 
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True