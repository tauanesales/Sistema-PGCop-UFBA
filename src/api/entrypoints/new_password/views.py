from fastapi import APIRouter, Depends, status
from src.api.database.session import get_db
from src.api.entrypoints.new_password.schema import NewPasswordChange, NewPasswordCodeAuth, NewPasswordRequest
from src.api.services.new_password import ServiceNewPassword
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=NewPasswordChange, status_code=status.HTTP_200_OK)
def set_new_password(request: NewPasswordChange, db: Session = Depends(get_db)):
    return ServiceNewPassword.set_new_password(db, request.email)


@router.post("/auth", response_model=NewPasswordCodeAuth, status_code=status.HTTP_200_OK)
def authenticate(request: NewPasswordCodeAuth, db: Session = Depends(get_db)):
    return ServiceNewPassword.authenticate(db, request.email, request.token)


@router.post("/createToken", response_model=NewPasswordRequest, status_code=status.HTTP_201_CREATED)
def create_token(request: NewPasswordRequest, db: Session = Depends(get_db)):
    return ServiceNewPassword.create_code(db, request.email)
    

