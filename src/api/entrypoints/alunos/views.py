from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from sqlalchemy.future import select
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import List, Optional
import os

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.session import get_repo
from src.api.entrypoints.alunos.schema import AlunoInDB, AlunoNovo
from src.api.entrypoints.tarefas.schema import TarefaInDB
from src.api.exceptions.credentials_exception import NaoAutorizadoException
from src.api.services.aluno import ServicoAluno
from src.api.services.tarefa import ServiceTarefa
from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico
from src.api.utils.enums import TipoUsuarioEnum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Buscar valores das variáveis de ambiente
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class TokenData(BaseModel):
    username: Optional[str] = None
    tipo_usuario: Optional[str] = None

async def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_repo)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise NaoAutorizadoException()
        token_data = TokenData(username=username)
    except JWTError:
        raise NaoAutorizadoException()

    # Buscar o usuário no banco de dados
    result = await session.execute(
        select(Aluno).where(Aluno.email == token_data.username)
    )
    usuario = result.scalars().first()
    if not usuario:
        raise NaoAutorizadoException()
    
    token_data.tipo_usuario = usuario.usuario.tipo_usuario.titulo
    return token_data

@router.post("/", response_model=AlunoInDB, status_code=status.HTTP_201_CREATED)
async def criar_aluno(aluno: AlunoNovo, repository=Depends(get_repo())):
    return await ServicoAluno(repository).criar(aluno)

@router.get("/{aluno_id}", response_model=AlunoInDB)
async def get_aluno(aluno_id: int, repository=Depends(get_repo())):
    return await ServicoAluno(repository).buscar_dados_in_db_por_id(aluno_id)

@router.delete(
    "/{aluno_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def deletar_aluno_por_id(
    aluno_id: int, token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    logger.info(f"Solicitado deleção de {aluno_id=} | Autenticando usuário atual.")
    coordenador: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token, tipo_usuario=TipoUsuarioEnum.COORDENADOR)
    logger.info(
        f"{aluno_id=} {coordenador.id=} | "
        f"Tipo usuário atual é {coordenador.usuario.tipo_usuario.titulo}."
    )
    if coordenador.usuario.tipo_usuario.titulo != TipoUsuarioEnum.COORDENADOR:
        raise NaoAutorizadoException()
    return await ServicoAluno(repository).deletar(aluno_id)

@router.delete("/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def deletar_aluno_atual(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    aluno: Aluno = await ServicoTipoUsuarioGenerico(repository).buscar_usuario_atual(
        token=token, tipo_usuario=TipoUsuarioEnum.ALUNO
    )
    return await ServicoAluno(repository).deletar(aluno.id)

@router.get("/cpf/{aluno_cpf}", response_model=AlunoInDB)
async def get_aluno_cpf(aluno_cpf: str, repository=Depends(get_repo()), token: str = Depends(oauth2_scheme)):
    professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)

    if professor.usuario.tipo_usuario.titulo not in [
        TipoUsuarioEnum.COORDENADOR,
        TipoUsuarioEnum.PROFESSOR,
    ]:
        raise NaoAutorizadoException()
    else:
        return await ServicoAluno(repository).buscar_aluno_por_cpf(aluno_cpf)

@router.get("/email/{aluno_email}", response_model=AlunoInDB)
async def get_aluno_email(aluno_email: str, repository=Depends(get_repo())):
    return await ServicoAluno(repository).buscar_dados_in_db_por_email(aluno_email)

@router.put("/{aluno_id}/remover-orientador/", response_model=AlunoInDB)
async def remover_orientador_aluno(
    aluno_id: int, token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    logger.info(
        f"Solicitado remoção do orientador do {aluno_id=} | Autenticando usuário atual."
    )
    coordenador_ou_professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)
    logger.info(
        f"{aluno_id=} {coordenador_ou_professor.id=} | "
        f"Tipo usuário atual é {coordenador_ou_professor.usuario.tipo_usuario.titulo}."
    )
    if (
        coordenador_ou_professor.usuario.tipo_usuario.titulo
        != TipoUsuarioEnum.COORDENADOR
    ) and (
        coordenador_ou_professor.usuario.tipo_usuario.titulo
        != TipoUsuarioEnum.PROFESSOR
    ):
        raise NaoAutorizadoException()

    return await ServicoAluno(repository).remover_orientador(aluno_id)

# Nova rota criada conforme orientação de tauane
@router.get("/tarefas", response_model=List[TarefaInDB])
async def obter_tarefas_do_aluno(current_user: TokenData = Depends(get_current_user), repository=Depends(get_repo())):
    if current_user.tipo_usuario != TipoUsuarioEnum.ALUNO:
        raise NaoAutorizadoException()
    
    aluno: Aluno = await ServicoTipoUsuarioGenerico(repository).buscar_usuario_atual(
        token=current_user.username, tipo_usuario=TipoUsuarioEnum.ALUNO
    )
    return await ServiceTarefa(repository).buscar_tarefas_por_aluno(aluno.id)





# from fastapi import APIRouter, Depends, status
# from fastapi.security import OAuth2PasswordBearer
# from loguru import logger

# from src.api.database.models.aluno import Aluno
# from src.api.database.models.professor import Professor
# from src.api.database.session import get_repo
# from src.api.entrypoints.alunos.schema import AlunoInDB, AlunoNovo
# from src.api.exceptions.credentials_exception import NaoAutorizadoException
# from src.api.services.aluno import ServicoAluno
# from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico
# from src.api.utils.enums import TipoUsuarioEnum

# router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @router.post("/", response_model=AlunoInDB, status_code=status.HTTP_201_CREATED)
# async def criar_aluno(aluno: AlunoNovo, repository=Depends(get_repo())):
#     return await ServicoAluno(repository).criar(aluno)


# @router.get("/{aluno_id}", response_model=AlunoInDB)
# async def get_aluno(aluno_id: int, repository=Depends(get_repo())):
#     return await ServicoAluno(repository).buscar_dados_in_db_por_id(aluno_id)


# @router.delete(
#     "/{aluno_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
# )
# async def deletar_aluno_por_id(
#     aluno_id: int, token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
# ):
#     logger.info(f"Solicitado deleção de {aluno_id=} | Autenticando usuário atual.")
#     coordenador: Professor = await ServicoTipoUsuarioGenerico(
#         repository
#     ).buscar_usuario_atual(token=token, tipo_usuario=TipoUsuarioEnum.COORDENADOR)
#     logger.info(
#         f"{aluno_id=} {coordenador.id=} | "
#         f"Tipo usuário atual é {coordenador.usuario.tipo_usuario.titulo}."
#     )
#     if coordenador.usuario.tipo_usuario.titulo != TipoUsuarioEnum.COORDENADOR:
#         raise NaoAutorizadoException()
#     return await ServicoAluno(repository).deletar(aluno_id)


# @router.delete("/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
# async def deletar_aluno_atual(
#     token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
# ):
#     aluno: Aluno = await ServicoTipoUsuarioGenerico(repository).buscar_usuario_atual(
#         token=token, tipo_usuario=TipoUsuarioEnum.ALUNO
#     )
#     return await ServicoAluno(repository).deletar(aluno.id)


# @router.get("/cpf/{aluno_cpf}", response_model=AlunoInDB)
# async def get_aluno_cpf(aluno_cpf: str, repository=Depends(get_repo()),token: str = Depends(oauth2_scheme)):
#     professor: Professor = await ServicoTipoUsuarioGenerico(
#         repository
#     ).buscar_usuario_atual(token=token)

#     if professor.usuario.tipo_usuario.titulo not in [
#         TipoUsuarioEnum.COORDENADOR,
#         TipoUsuarioEnum.PROFESSOR,
#     ]:
#         raise NaoAutorizadoException()
#     else:
#         return await ServicoAluno(repository).buscar_aluno_por_cpf(aluno_cpf)


# @router.get("/email/{aluno_email}", response_model=AlunoInDB)
# async def get_aluno_email(aluno_email: str, repository=Depends(get_repo())):
#     return await ServicoAluno(repository).buscar_dados_in_db_por_email(aluno_email)


# @router.put("/{aluno_id}/remover-orientador/", response_model=AlunoInDB)
# async def remover_orientador_aluno(
#     aluno_id: int, token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
# ):
#     logger.info(
#         f"Solicitado remoção do orientador do {aluno_id=} | Autenticando usuário atual."
#     )
#     coordenador_ou_professor: Professor = await ServicoTipoUsuarioGenerico(
#         repository
#     ).buscar_usuario_atual(token=token)
#     logger.info(
#         f"{aluno_id=} {coordenador_ou_professor.id=} | "
#         f"Tipo usuário atual é {coordenador_ou_professor.usuario.tipo_usuario.titulo}."
#     )
#     if (
#         coordenador_ou_professor.usuario.tipo_usuario.titulo
#         != TipoUsuarioEnum.COORDENADOR
#     ) and (
#         coordenador_ou_professor.usuario.tipo_usuario.titulo
#         != TipoUsuarioEnum.PROFESSOR
#     ):
#         raise NaoAutorizadoException()

#     return await ServicoAluno(repository).remover_orientador(aluno_id)
