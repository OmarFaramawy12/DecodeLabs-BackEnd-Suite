from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Step-1 Creating The Database URL (Connection to Database File)
DATABASE_URL = os.getenv("DATABASE_URL")

# Step-2 Creating The Engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False})

# Step-3 Creating The Session Local Class
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine)
# Step-4 Creating The Base Class (Database models will inherit from Base class)
Base = declarative_base()

''' 
Step-5 Creating A Dependency To Get The Database Session
Every time a request is made to the API, 
a new database session will be created and closed after
the request is completed.
 '''

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()