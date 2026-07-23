# backend/app/api/v1/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
 
is_railway = os.getenv("RAILWAY_ENVIRONMENT_NAME")
if not is_railway:
    # Find .env file - could be in backend/ or project root
    env_path = None
    for path in [".env", "../.env", "../../.env"]:
        if os.path.exists(path):
            env_path = path
            break
    
    if env_path:
        print(f"[CONSOLE-DB] Loading .env from: {os.path.abspath(env_path)}")
        load_dotenv(env_path)
    else:
        print("[CONSOLE-DB] No .env file found - using system environment variables")
else:
    print("[CONSOLE-DB] Railway environment detected - using injected variables")

# Get DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

print(f"[CONSOLE-DB] DATABASE_URL found: {bool(DATABASE_URL)}")
if DATABASE_URL:
    print(f"[CONSOLE-DB] Connection string (first 60 chars): {DATABASE_URL[:60]}...")

if not DATABASE_URL:
    if is_railway:
        print("[CONSOLE-DB] ❌ ERROR: DATABASE_URL not found in Railway environment!")
        print("[CONSOLE-DB] Fix: Ensure PostgreSQL plugin is connected in Railway dashboard")
    else:
        print("[CONSOLE-DB] ⚠️  DATABASE_URL not found in local environment")
        print("[CONSOLE-DB] Create a .env file with: DATABASE_URL=postgresql://...")
    
    # Don't silently fall back - make it obvious
    raise ValueError(
        "DATABASE_URL is required. "
        f"{'Connect PostgreSQL plugin in Railway' if is_railway else 'Create .env file with DATABASE_URL'}"
    )

# Convert postgres:// to postgresql:// for SQLAlchemy 2.0
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Yield a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()