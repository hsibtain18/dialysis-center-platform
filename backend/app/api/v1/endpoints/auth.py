from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Login successful", "token": "dummy-jwt-token"}




@router.post("/second-login")
def login():
    return {"message": "Login asd", "token": "dummy-jwt-token"}