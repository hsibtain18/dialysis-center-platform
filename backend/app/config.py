# backend/app/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dialysis Center Management System"
    API_V1_STR: str = "/api/v1"
    
    # Database connection string (configured automatically in Railway)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:MRYKhvgplMpmukPSpEbfXHohrrIHQeEg@postgres.railway.internal:5432/railway")
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    class Config:
        env_file = ".env"

settings = Settings()