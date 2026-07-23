import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# 1. ALWAYS load .env first for local development
is_railway = os.getenv("RAILWAY_ENVIRONMENT_NAME")
if not is_railway:
    for path in [".env", "../.env", "../../.env"]:
        if os.path.exists(path):
            load_dotenv(path)
            break

print("\n" + "="*100)
print("[CONSOLE-DB] ENVIRONMENT VARIABLES AVAILABLE AT STARTUP")
print("="*100 + "\n")

all_vars = sorted(os.environ.items())
print(f"Total environment variables: {len(all_vars)}\n")

print("="*100)
print("[CONSOLE-DB] DATABASE-RELATED VARIABLES:")
print("="*100 + "\n")

# Filter database-related variables
db_related = {k: v for k, v in all_vars if any(x in k.upper() for x in ['DATABASE', 'DB', 'PG', 'SQL'])}

if db_related:
    # FIXED: Added .items() to fix the unpacking crash
    for key, value in db_related.items():
        if 'PASSWORD' in key.upper():
            display = f"{'*' * 15} (length: {len(value)})"
        else:
            display = value if len(value) <= 80 else value[:80] + "..."
        print(f"  {key:<40} = {display}")
else:
    print("  ⚠️  NO DATABASE VARIABLES FOUND!\n")

print("\n" + "="*100)

# 2. Get or construct DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("[CONSOLE-DB] DATABASE_URL not found directly, attempting to construct from PG* variables...\n")
    
    pguser = os.getenv("PGUSER")
    pgpassword = os.getenv("PGPASSWORD")
    pghost = os.getenv("PGHOST")
    pgport = os.getenv("PGPORT", "5432")
    pgdatabase = os.getenv("PGDATABASE")
    
    if pguser and pgpassword and pghost:
        DATABASE_URL = f"postgresql://{pguser}:{pgpassword}@{pghost}:{pgport}/{pgdatabase or 'railway'}"
        print(f"[CONSOLE-DB] ✅ Constructed DATABASE_URL from PG variables:\n  {DATABASE_URL[:80]}...\n")
    else:
        print("[CONSOLE-DB] ❌ Cannot construct DATABASE_URL - missing PG variables!\n")

# Final check
if not DATABASE_URL:
    print("[CONSOLE-DB] ⚠️  WARNING: No DATABASE_URL available!")
    print("[CONSOLE-DB] App starting without database connection for debugging...\n")
    DATABASE_URL = None
else:
    print(f"[CONSOLE-DB] ✅ Using DATABASE_URL: {DATABASE_URL[:80]}...\n")

print("="*100 + "\n")

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