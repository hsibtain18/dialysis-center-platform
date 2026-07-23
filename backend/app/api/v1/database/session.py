# backend/app/api/v1/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ GRAB DATABASE_URL ONCE AT MODULE LOAD TIME
# Railway automatically injects this; don't check for it conditionally at runtime
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate it exists - fail fast if not configured
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Ensure it's configured in Railway dashboard under Variables."
    )

print(f"[CONSOLE-DB] DATABASE_URL loaded successfully (first 50 chars): {DATABASE_URL[:50]}...")

# Safe modification because SQLAlchemy 2.0 requires "postgresql://" instead of "postgres://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print("[CONSOLE-DB] Converted 'postgres://' to 'postgresql://' for SQLAlchemy 2.0 compatibility")

# ✅ CREATE ENGINE ONCE AT MODULE LOAD TIME
# Reusing the same engine across all requests is more efficient
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Keeps connections alive; good for cloud services
    echo=False  # Set to True for SQL debugging if needed
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ SIMPLE DEPENDENCY INJECTION - no complex logic
def get_db():
    """Yield a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()