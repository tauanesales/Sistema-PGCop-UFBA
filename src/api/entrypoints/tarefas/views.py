from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.entrypoints.tarefas.schema import TarefaBase, TarefaInDB
from src.api.services.tarefa import ServiceTarefa

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/tarefas", response_model=TarefaInDB, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: TarefaBase, db: Session = Depends(get_db)):
   return ServiceTarefa.criar_tarefa(db, tarefa)

@router.put("/tarefas/{tarefa_id}", response_model=TarefaInDB)
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaBase, db: Session = Depends(get_db)):
    return ServiceTarefa.atualizar_tarefa(db, tarefa_id, tarefa.dict())

@router.delete("/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    ServiceTarefa.deletar_tarefa(db, tarefa_id)
    return {"ok": True}

@router.get("/tarefas/{tarefa_id}", response_model=TarefaInDB)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    return ServiceTarefa.obter_tarefa(db, tarefa_id)


