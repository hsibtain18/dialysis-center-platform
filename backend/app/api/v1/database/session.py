# backend/app/api/v1/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Safely look for local testing configurations
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback string to satisfy SQLAlchemy during isolated build/pre-compile steps
if not DATABASE_URL:
    DATABASE_URL = "postgresql://placeholder_user:placeholder_pass@localhost:5432/placeholder_db"

# Cloud database driver sanitization
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Establish connection configuration pool
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()