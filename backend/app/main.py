# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1.router import api_router
import os
import sys
 
print("\n" + "="*100)
print("[STARTUP-DEBUG] ALL ENVIRONMENT VARIABLES AT APPLICATION START")
print("="*100)
 
# Get all environment variables
all_vars = sorted(os.environ.items())
 
print(f"\nTotal Variables: {len(all_vars)}\n")
 
# Print each variable
for key, value in all_vars:
    # Hide sensitive values
    if any(sensitive in key.upper() for sensitive in ['PASSWORD', 'SECRET', 'TOKEN', 'KEY', 'CREDENTIAL']):
        display = f"{'*' * 20} (hidden, length: {len(value)})"
    else:
        # Truncate long values
        if len(value) > 100:
            display = value[:100] + f"... (truncated, total length: {len(value)})"
        else:
            display = value
    
    print(f"  {key:<40} = {display}")
 
print("\n" + "="*100)
print(f"[STARTUP-DEBUG] DATABASE_URL exists: {bool(os.getenv('DATABASE_URL'))}")
print(f"[STARTUP-DEBUG] RAILWAY_ENVIRONMENT_NAME: {os.getenv('RAILWAY_ENVIRONMENT_NAME', 'NOT SET')}")
print("="*100 + "\n")
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS for your local and production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-production-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the centralized modular router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"status": "healthy", "service": settings.PROJECT_NAME}