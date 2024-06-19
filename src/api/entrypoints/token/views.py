from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.session import get_repo
from src.api.entrypoints.token.schema import Token
from src.api.services.auth import ServicoAuth

router = APIRouter()


@router.post("/", response_model=Token)
async def login_para_acessar_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repository: AsyncSession = Depends(get_repo()),
) -> Token:
    return await ServicoAuth(repository).login_para_acessar_token(
        form_data.username, form_data.password
    )
