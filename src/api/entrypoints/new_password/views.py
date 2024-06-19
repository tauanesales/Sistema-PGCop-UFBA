from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.session import get_repo
from src.api.entrypoints.new_password.schema import (
    NewPasswordChange,
    NewPasswordCodeAuth,
    NewPasswordRequest,
)
from src.api.services.new_password import ServiceNewPassword

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def set_new_password(request: NewPasswordChange, db: AsyncSession = Depends(get_repo)):
    await ServiceNewPassword.set_new_password(
        db, request.email, request.nova_senha, request.token
    )


@router.post("/auth", status_code=status.HTTP_200_OK)
async def authenticate(request: NewPasswordCodeAuth, db: AsyncSession = Depends(get_repo)):
    await ServiceNewPassword.authenticate(db, request.email, request.token)


@router.post("/create_token", status_code=status.HTTP_201_CREATED)
async def create_token(request: NewPasswordRequest, db: AsyncSession = Depends(get_repo)):
    await ServiceNewPassword.create_token(db, request.email)
