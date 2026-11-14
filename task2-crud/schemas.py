'''
This file defines the Pydantic models (schemas) for the API.
Pydantic models — these define what the API accepts and returns.
Difference Between SQLAlchemy and Pydantic Models:
    1- models.py  = database shape
    2- schemas.py (pydantic Model) = API shape (what clients send/receive)
'''

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

# BaseModel is the base class for all Pydantic models. It provides data validation and serialization.
class UserBase(BaseModel):
    username: str
    email: EmailStr
    age: Optional[int] = None  # Age is optional

   
    
# Step-2: UserCreate inherits from UserBase and adds any additional fields required for creating a user.
class UserCreate(UserBase):
    @field_validator('age')
    @classmethod
    def age_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Age must be greater than 0')
        return v

    @field_validator('username')
    @classmethod
    def username_must_be_valid(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Username must be at least 2 characters')
        return v.strip()
    
# Step-2: UserUpdate inherits from UserBase and adds any additional fields required for updating a user.
class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    is_active: Optional[bool] = None


# Step-3: UserResponse inherits from UserBase and adds any additional fields required for returning a user in API responses.
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Tells Pydantic to read data from ORM objects (like SQLAlchemy models)