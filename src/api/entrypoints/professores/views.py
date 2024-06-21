from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.api.database.models.professor import Professor
from src.api.database.session import get_repo
from src.api.entrypoints.professores.schema import (
    ProfessorAtualizado,
    ProfessorInDB,
    ProfessorNovo,
)
from src.api.services.professor import ServiceProfessor
from src.api.services.tipo_usuario import ServicoTipoUsuario
from src.api.utils.enums import TipoUsuarioEnum

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=ProfessorInDB, status_code=status.HTTP_201_CREATED)
async def criar_professor(professor: ProfessorNovo, repository=Depends(get_repo())):
    return await ServiceProfessor(repository).criar(novo_professor=professor)


@router.get("/me", response_model=ProfessorInDB)
async def read_professor_me(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    return await ServiceProfessor(repository).buscar_atual(token)


@router.get("/todos", response_model=List[ProfessorInDB])
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
    return await ServiceProfessor(repository).deletar(professor_id)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_professor_atual(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    professor: Professor = await ServicoTipoUsuario(repository).buscar_usuario_atual(
        token=token, tipo_usuario=TipoUsuarioEnum.PROFESSOR
    )
    return await ServiceProfessor(repository).deletar(professor.id)


@router.put("/{professor_id}", response_model=ProfessorInDB)
async def atualizar_professor(
    professor_id: int, professor: ProfessorAtualizado, repository=Depends(get_repo())
):
    return await ServiceProfessor(repository).atualizar_professor(
        professor_id, professor
    )


@router.get("/email/{email}", response_model=ProfessorInDB)
async def obter_professor_por_email(email: str, repository=Depends(get_repo())):
    return await ServiceProfessor(repository).buscar_dados_in_db_por_email(email=email)
