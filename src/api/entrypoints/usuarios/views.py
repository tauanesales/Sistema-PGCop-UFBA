from typing import Union

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError

from src.api.database.session import get_repo
from src.api.entrypoints.alunos.schema import AlunoAtualizado, AlunoInDB
from src.api.entrypoints.professores.schema import ProfessorAtualizado, ProfessorInDB
from src.api.exceptions.value_error_validation_exception import InvalidLattesError
from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=Union[AlunoInDB, ProfessorInDB])
async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    return await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_dados_in_db_usuario_atual(token=token)


@router.put("/", response_model=ProfessorInDB)
async def atualizar_usuario(
    usuario_tipo_generico: Union[AlunoAtualizado, ProfessorAtualizado],
    token: str = Depends(oauth2_scheme),
    repository=Depends(get_repo()),
):
    try:
        return await ServicoTipoUsuarioGenerico(repository).atualizar(
            usuario_tipo_generico, token
        )
    except InvalidLattesError as err:
        raise RequestValidationError([{
            "detail": [{
                "type": "value_error",
                "loc": ("body", "lattes"),
                "msg": err.args[0]
            }]
        }])
