from datetime import date
from pydantic import BaseModel,constr
from typing import Literal,Optional


class TarefaBase(BaseModel):
    descricao: constr(max_length=100)
    completada: int
    data_prazo: date
    aluno_id: int
    last_notified: Optional[date] = None
    data_conclusao: Optional[date] = None
    nome: constr(max_length=100)


class TarefaInDB(TarefaBase):
    id: int

    class Config:
        from_attributes = True
