from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from src.api.database.models.professor import Professor
from src.api.database.session import get_repo
from src.api.entrypoints.alunos.schema import AlunoInDB
from src.api.entrypoints.professores.schema import (
    ProfessorInDB,
    ProfessorNovo,
    ProfessorResponse,
)
from src.api.exceptions.credentials_exception import NaoAutorizadoException
from src.api.services.aluno import ServicoAluno
from src.api.services.professor import ServiceProfessor
from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico
from src.api.utils.enums import TipoUsuarioEnum

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=ProfessorInDB, status_code=status.HTTP_201_CREATED)
async def criar_professor(professor: ProfessorNovo, repository=Depends(get_repo())):
    return await ServiceProfessor(repository).criar(novo_professor=professor)


@router.get("/todos", response_model=List[ProfessorResponse])
async def obter_todos_professores(repository=Depends(get_repo())):
    return await ServiceProfessor(repository).obter_professores()


@router.get("/{professor_id}", response_model=ProfessorInDB)
async def buscar_professor_por_id(professor_id: int, repository=Depends(get_repo())):
    return await ServiceProfessor(repository).buscar_dados_in_db_por_id(
        professor_id=professor_id
    )


@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_professor(
    professor_id: int,
    token: str = Depends(oauth2_scheme),
    repository=Depends(get_repo()),
):
    logger.info(f"Solicitado deleção de {professor_id=} | Autenticando usuário atual.")
    coordenador: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token, tipo_usuario=TipoUsuarioEnum.COORDENADOR)
    logger.info(
        f"{professor_id=} {coordenador.id=} | "
        f"Tipo usuário atual é {coordenador.usuario.tipo_usuario.titulo}."
    )
    if coordenador.usuario.tipo_usuario.titulo != TipoUsuarioEnum.COORDENADOR:
        raise NaoAutorizadoException()

    return await ServiceProfessor(repository).deletar(professor_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_professor_atual(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    logger.info("Solicitado deleção por token | Autenticando usuário atual.")
    professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token, tipo_usuario=TipoUsuarioEnum.PROFESSOR)
    logger.info(
        f"{professor.id=} | "
        f"Tipo usuário atual é {professor.usuario.tipo_usuario.titulo}."
    )
    return await ServiceProfessor(repository).deletar(professor.id)


@router.get("/email/{email}", response_model=ProfessorInDB)
async def obter_professor_por_email(email: str, repository=Depends(get_repo())):
    return await ServiceProfessor(repository).buscar_dados_in_db_por_email(email=email)


@router.get("/orientandos/{professor_id}", response_model=List[AlunoInDB])
async def get_orientandos_por_professor_id(
    professor_id: int,
    token: str = Depends(oauth2_scheme),
    repository=Depends(get_repo()),
):
    logger.info(
        f"Solicitado lista de orientandos do {professor_id=}"
        f" | Autenticando usuário atual."
    )
    coordenador: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token, tipo_usuario=TipoUsuarioEnum.COORDENADOR)
    logger.info(
        f"{professor_id=} {coordenador.id=} | "
        f"Tipo usuário atual é {coordenador.usuario.tipo_usuario.titulo}."
    )
    if coordenador.usuario.tipo_usuario.titulo != TipoUsuarioEnum.COORDENADOR:
        raise NaoAutorizadoException()
    return await ServicoAluno(repository).buscar_alunos_por_orientador(professor_id)


@router.get("/orientandos/", response_model=List[AlunoInDB])
async def get_orientandos_por_token(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    logger.info(
        "Solicitado lista de orientandos por token | Autenticando usuário atual."
    )
    professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token, tipo_usuario=TipoUsuarioEnum.PROFESSOR)
    logger.info(
        f"{professor.id=} | "
        f"Tipo usuário atual é {professor.usuario.tipo_usuario.titulo}."
    )
    return await ServicoAluno(repository).buscar_alunos_por_orientador(professor.id)
