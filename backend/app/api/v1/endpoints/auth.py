# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
import os

print("[CONSOLE-AUTH] Loading auth.py router module...")

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-key-for-local-dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class UserRegisterInput(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLoginInput(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)

@router.post("/register")
def register_user(user_in: UserRegisterInput, db: Session = Depends(get_db)):
    print(f"[CONSOLE-AUTH] Incoming register request for email: {user_in.email}")
    try:
        print("[CONSOLE-AUTH] Checking user array state...")
        all_current_users = db.query(User).all()
        print(f"[CONSOLE-AUTH] Total records initially found in table: {len(all_current_users)}")
        
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            print(f"[CONSOLE-AUTH] Register failed: Email {user_in.email} already exists.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Email is already registered."
            )
        
        print("[CONSOLE-AUTH] Hashing password and initiating record staging...")
        new_user = User(
            email=user_in.email,
            password=pwd_context.hash(user_in.password),
            first_name=user_in.first_name,
            last_name=user_in.last_name
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"[CONSOLE-AUTH] Success! User committed with UUID: {new_user.id}")
        
        return {
            "message": "Successfully connected and verified!",
            "new_user_id": str(new_user.id),
            "total_users_in_db": len(all_current_users) + 1
        }
    except Exception as e:
        print(f"[CONSOLE-AUTH] Exception caught during execution: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Trace: {str(e)}")

@router.post("/login", response_model=TokenResponse)
def login_user(user_in: UserLoginInput, db: Session = Depends(get_db)):
    print(f"[CONSOLE-AUTH] Incoming login attempt for email: {user_in.email}")
    try:
        user = db.query(User).filter(User.email == user_in.email).first()
        if not user:
            print("[CONSOLE-AUTH] Login failed: User email not found in database.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
            
        print("[CONSOLE-AUTH] User found. Validating password hash...")
        if not pwd_context.verify(user_in.password, user.password):
            print("[CONSOLE-AUTH] Login failed: Password hash verification mismatch.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            print("[CONSOLE-AUTH] Login failed: User active status evaluates to False.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user account"
            )
            
        print("[CONSOLE-AUTH] Credentials verified. Minting JWT Access token...")
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }
    except Exception as e:
        print(f"[CONSOLE-AUTH] Login Exception caught: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Trace: {str(e)}")