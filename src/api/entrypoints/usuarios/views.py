from typing import Union

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.api.database.session import get_repo
from src.api.entrypoints.alunos.schema import AlunoInDB
from src.api.entrypoints.professores.schema import ProfessorInDB
from src.api.services.tipo_usuario import ServicoTipoUsuario

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=Union[AlunoInDB, ProfessorInDB])
async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    return await ServicoTipoUsuario(repository).obter_usuario_atual(token=token)
