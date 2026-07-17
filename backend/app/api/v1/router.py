# backend/app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import auth

api_router = APIRouter()

# Register endpoint files here
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])