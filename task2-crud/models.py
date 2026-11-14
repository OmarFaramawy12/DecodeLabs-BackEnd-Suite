from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

# Models Class defines the structure of the database tables and how they relate to each other.
# SQLAlchemy uses these models to create the database schema and to perform CRUD operations on the database.
# SQLAlchemy Converts these python models into SQL statements that can be executed against the database.
class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, 
        primary_key=True,
        index=True  # Index for faster lookups
    )
    username = Column(
        String(50),
        unique=True,        # No two users can share a username
        nullable=False,     # Cannot be empty
        index=True
    )

    email = Column(
        String(255), 
        unique=True, 
        nullable=False,
        index=True
    )
    age = Column(
        Integer,
        nullable=True       # Age is optional
    )

    is_active = Column(
        Boolean, 
        default=True
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now()
    )