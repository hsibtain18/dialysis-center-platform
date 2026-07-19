# backend/app/api/v1/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

print("[CONSOLE-DB] Loading session.py module...")
load_dotenv()

Base = declarative_base()

def get_engine():
    url = os.getenv("DATABASE_URL")
    print(f"[CONSOLE-DB] os.getenv('DATABASE_URL') returned: {url if not url else 'FOUND_STRING_MASKED'}")
    
    if not url:
        print("[CONSOLE-DB] WARNING: No DATABASE_URL found. Using placeholder fallback!")
        url = "postgresql://placeholder_user:placeholder_pass@127.0.0.1:5432/placeholder_db"
        
    if url.startswith("postgres://"):
        print("[CONSOLE-DB] Normalizing postgres:// schema to postgresql://")
        url = url.replace("postgres://", "postgresql://", 1)
        
    return create_engine(url, pool_pre_ping=True)

def get_db():
    print("[CONSOLE-DB] Yielding new database Session Local instance...")
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
        print("[CONSOLE-DB] Database session completed cleanly.")
    except Exception as e:
        print(f"[CONSOLE-DB] CRITICAL error during active session yield: {e}")
        raise
    finally:
        db.close()
        print("[CONSOLE-DB] Database session connection closed.")