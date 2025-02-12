from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings  # Ensure this import is correct
import os


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create a database engine
engine = create_engine(settings.DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function for database session


def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide session
    finally:
        db.close()  # Close session after use
