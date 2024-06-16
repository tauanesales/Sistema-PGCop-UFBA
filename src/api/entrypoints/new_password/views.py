from fastapi import APIRouter, Depends, status
from src.api.database.session import get_db
from src.api.entrypoints.new_password.schema import NewPasswordChange, NewPasswordCodeAuth, NewPasswordRequest
from src.api.services.new_password import ServiceNewPassword
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def set_new_password(request: NewPasswordChange, db: Session = Depends(get_db)):
    ServiceNewPassword.set_new_password(db, request.email, request.nova_senha, request.token)


@router.post("/auth", status_code=status.HTTP_200_OK)
async def authenticate(request: NewPasswordCodeAuth, db: Session = Depends(get_db)):
    ServiceNewPassword.authenticate(db, request.email, request.token)


@router.post("/create_token", status_code=status.HTTP_201_CREATED)
async def create_token(request: NewPasswordRequest, db: Session = Depends(get_db)):
    ServiceNewPassword.create_token(db, request.email)
    

