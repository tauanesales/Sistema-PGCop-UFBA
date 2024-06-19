from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.session import get_repo
from src.api.entrypoints.tarefas.schema import TarefaBase, TarefaInDB
from src.api.services.tarefa import ServiceTarefa

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=TarefaInDB, status_code=status.HTTP_201_CREATED)
async def criar_tarefa(tarefa: TarefaBase, db: AsyncSession = Depends(get_repo)):
    return await ServiceTarefa.criar_tarefa(db, tarefa)


@router.put("/{tarefa_id}", response_model=TarefaInDB)
async def atualizar_tarefa(tarefa_id: int, tarefa: TarefaBase, db: AsyncSession = Depends(get_repo)):
    return await ServiceTarefa.atualizar_tarefa(db, tarefa_id, tarefa)


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tarefa(tarefa_id: int, db: AsyncSession = Depends(get_repo)):
    await ServiceTarefa.deletar_tarefa(db, tarefa_id)
    return {"ok": True}


@router.get("/{tarefa_id}", response_model=TarefaInDB)
async def obter_tarefa(tarefa_id: int, db: AsyncSession = Depends(get_repo)):
    return await ServiceTarefa.obter_tarefa(db, tarefa_id)


@router.get("/aluno/{aluno_id}", response_model=List[TarefaInDB])
async def get_aluno_tarefas(aluno_id: int, db: AsyncSession = Depends(get_repo)):
    return await ServiceTarefa.obter_tarefas_por_aluno(db, aluno_id)
