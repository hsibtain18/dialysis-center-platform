# backend/app/api/v1/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Grabs the internal DATABASE_URL from Railway dashboard automatically
DATABASE_URL = os.getenv("DATABASE_URL")

# Safe modification because SQLAlchemy 2.0 requires "postgresql://" instead of "postgres://"
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # Keeps connections alive on cloud services
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# The dependency injected function we will pass to our API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()