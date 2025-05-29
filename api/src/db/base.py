from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import Session
from sqlalchemy import create_engine
import os

# Define the base class for models
Base = declarative_base()
# Load the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
# Create the database engine
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session