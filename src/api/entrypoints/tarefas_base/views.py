from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from src.api.database.models.professor import Professor
from src.api.database.session import get_repo
from src.api.entrypoints.tarefas_base.schema import (
    CursoEnum,
    TarefaBaseAtualizada,
    TarefaBaseBase,
    TarefaBaseInDB,
)
from src.api.exceptions.credentials_exception import NaoAutorizadoException
from src.api.services.tarefa_base import ServiceTarefaBase
from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico
from src.api.utils.enums import TipoUsuarioEnum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=TarefaBaseInDB, status_code=status.HTTP_201_CREATED)
async def criar_tarefa_base(tarefa: TarefaBaseBase, repository=Depends(get_repo())):
    return await ServiceTarefaBase(repository).criar_tarefa_base(tarefa)


@router.put("/{tarefa_id}", response_model=TarefaBaseInDB)
async def atualizar_tarefa_base(
    tarefa_id: int,
    tarefa_base_atualizada: TarefaBaseAtualizada,
    repository=Depends(get_repo()),
):
    return await ServiceTarefaBase(repository).atualizar_tarefa_base(
        tarefa_id, tarefa_base_atualizada
    )


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tarefa_base(tarefa_id: int, repository=Depends(get_repo())):
    return await ServiceTarefaBase(repository).deletar_tarefa_base(tarefa_id)


@router.get("/{tarefa_id}", response_model=TarefaBaseInDB)
async def buscar_tarefa_base(tarefa_id: int,token: str = Depends(oauth2_scheme), repository=Depends(get_repo())):
    professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)

    if professor.usuario.tipo_usuario.titulo not in [
        TipoUsuarioEnum.COORDENADOR,
        TipoUsuarioEnum.PROFESSOR,
    ]:
        raise NaoAutorizadoException()
    return await ServiceTarefaBase(repository).buscar_tarefa_base(tarefa_id)


@router.get("/curso/{curso}", response_model=List[TarefaBaseInDB])
async def buscar_tarefa_por_curso_base(
    curso: CursoEnum, repository=Depends(get_repo())
):
    return await ServiceTarefaBase(repository).buscar_tarefas_base_por_curso(curso)
