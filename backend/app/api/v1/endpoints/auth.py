# backend/app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.api.v1.database.session import get_db
from app.api.v1.models.user import User

router = APIRouter()

class UserRegisterInput(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

@router.post("/register")
def register_user(user_in: UserRegisterInput, db: Session = Depends(get_db)):
    # 1. Test Fetching Data from DB
    all_current_users = db.query(User).all()
    
    # 2. Duplicate Check
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email is already registered."
        )
    
    # 3. Insert New User Row
    new_user = User(
        email=user_in.email,
        password=user_in.password,  # Storing plain text for initial testing
        first_name=user_in.first_name,
        last_name=user_in.last_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Return verification showing the newly added ID and count of total records in DB
    return {
        "message": "Successfully connected and verified!",
        "new_user_id": str(new_user.id),
        "total_users_in_db": len(all_current_users) + 1
    }