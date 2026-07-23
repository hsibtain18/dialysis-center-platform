import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env for local development
is_railway = os.getenv("RAILWAY_ENVIRONMENT_NAME")
if not is_railway:
    for path in [".env", "../.env", "../../.env"]:
        if os.path.exists(path):
            load_dotenv(path)
            break

# Get or construct DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    pguser = os.getenv("PGUSER")
    pgpassword = os.getenv("PGPASSWORD")
    pghost = os.getenv("PGHOST")
    pgport = os.getenv("PGPORT", "5432")
    pgdatabase = os.getenv("PGDATABASE")
    
    if pguser and pgpassword and pghost:
        DATABASE_URL = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase or 'railway'}"

# Convert legacy postgres:// to postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engine & session factory
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

Base = declarative_base()

def get_db():
    """Yield a database session for each request."""
    if SessionLocal is None:
        raise RuntimeError(
            "Database not configured. Ensure DATABASE_URL is set in Railway Variables or .env file"
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()