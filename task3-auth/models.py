from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

# create a User model
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    )
    username = Column(
        String(50), 
        unique=True,
        nullable=False, 
        index=True, 
    )
    email = Column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False
    )
    # Storing the Hashed Password, not the plain text password
    password_hash = Column(
        String(255), 
        nullable=False
    )
    is_active = Column(
        Boolean, 
        default=True
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )