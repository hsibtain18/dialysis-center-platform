# backend/app/api/v1/database/session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Only read .env files locally. Let the cloud handle raw environment arrays directly!
if not os.getenv("RAILWAY_ENVIRONMENT_NAME"):
    print("[CONSOLE-DB] Local environment detected. Loading .env file...")
    load_dotenv()
else:
    print("[CONSOLE-DB] Cloud environment detected. Skipping local .env files.")

Base = declarative_base()

def get_engine():
    # Fetch straight from the execution context shell
    url = os.environ.get("DATABASE_URL")
    
    print(f"[CONSOLE-DB] Context check - DATABASE_URL exists: {bool(url)}")
    
    if not url:
        print("[CONSOLE-DB] CRITICAL FALLBACK TRIGGERED: Forcing explicit database string injection.")
        # COPY AND PASTE YOUR RAW DATABASE URL HERE DIRECTLY IF RAILWAY CONTINUES TO HIDE SYSTEM ARRAYS
        url = "postgresql://placeholder_user:placeholder_pass@127.0.0.1:5432/placeholder_db"
        
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
        
    return create_engine(url, pool_pre_ping=True)

def get_db():
    print("[CONSOLE-DB] Yielding new database Session Local instance...")
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(f"[CONSOLE-DB] Exception hit within block: {str(e)}")
        raise
    finally:
        db.close()