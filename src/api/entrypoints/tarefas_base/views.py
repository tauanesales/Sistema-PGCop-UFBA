from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.entrypoints.tarefas_base.schema import (
    CursoEnum,
    Tarefa_base_Base,
    Tarefa_base_InDB,
)
from src.api.services.tarefa_base import ServiceTarefaBase

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=Tarefa_base_InDB, status_code=status.HTTP_201_CREATED)
def criar_tarefa_base(tarefa: Tarefa_base_Base, db: Session = Depends(get_db)):
    return ServiceTarefaBase.criar_tarefa_base(db, tarefa)


@router.put("/{tarefa_id}", response_model=Tarefa_base_InDB)
def atualizar_tarefa_base(
    tarefa_id: int, tarefa: Tarefa_base_Base, db: Session = Depends(get_db)
):
    return ServiceTarefaBase.atualizar_tarefa_base(db, tarefa_id, tarefa.model_dump())


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa_base(tarefa_id: int, db: Session = Depends(get_db)):
    ServiceTarefaBase.deletar_tarefa_base(db, tarefa_id)
    return {"ok": True}


@router.get("/{tarefa_id}", response_model=Tarefa_base_InDB)
def obter_tarefa_base(tarefa_id: int, db: Session = Depends(get_db)):
    return ServiceTarefaBase.obter_tarefa_base(db, tarefa_id)


@router.get("/curso/{curso}", response_model=List[Tarefa_base_InDB])
def obter_tarefa_por_curso_base(curso: CursoEnum, db: Session = Depends(get_db)):
    return ServiceTarefaBase.obter_tarefas_base_por_curso(db, curso)
