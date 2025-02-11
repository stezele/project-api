from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure the connection string is correctly set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, fast_executemany=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
