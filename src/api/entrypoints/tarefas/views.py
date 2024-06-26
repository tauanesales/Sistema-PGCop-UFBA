from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from src.api.database.models.professor import Professor
from src.api.database.session import get_repo
from src.api.entrypoints.tarefas.schema import TarefaAtualizada, TarefaBase, TarefaInDB
from src.api.exceptions.credentials_exception import NaoAutorizadoException
from src.api.services.tarefa import ServiceTarefa
from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico
from src.api.utils.enums import TipoUsuarioEnum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=TarefaInDB, status_code=status.HTTP_201_CREATED)
async def criar_tarefa(tarefa: TarefaBase, repository=Depends(get_repo())):
    return await ServiceTarefa(repository).criar_tarefa(tarefa)


@router.put("/{tarefa_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def atualizar_tarefa(
    tarefa_id: int, tarefa: TarefaAtualizada, repository=Depends(get_repo())
):
    return await ServiceTarefa(repository).atualizar_tarefa(tarefa_id, tarefa)


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tarefa(tarefa_id: int, repository=Depends(get_repo())):
    await ServiceTarefa(repository).deletar_tarefa(tarefa_id)
    return {"ok": True}


@router.get("/{tarefa_id}", response_model=TarefaInDB)
async def buscar_tarefa(tarefa_id: int, repository=Depends(get_repo())):
    return await ServiceTarefa(repository).buscar_tarefa(tarefa_id)


@router.get("/aluno/{aluno_id}", response_model=list[TarefaInDB])
async def buscar_tarefas_por_aluno(
    aluno_id: int, token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    logger.info(
        f"Solicitado lista de tarefas do aluno {aluno_id=}"
        f" | Autenticando usuário atual."
    )

    pessoa: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)
    logger.info(
        f"{pessoa.id=} | " f"Tipo usuário atual é {pessoa.usuario.tipo_usuario.titulo}."
    )

    if pessoa.usuario.tipo_usuario.titulo == TipoUsuarioEnum.ALUNO:
        raise NaoAutorizadoException()
    return await ServiceTarefa(repository).buscar_tarefas_por_aluno(aluno_id)
