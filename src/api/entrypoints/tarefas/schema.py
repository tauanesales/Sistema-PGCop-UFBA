import datetime
from pydantic import BaseModel,constr
from typing import Literal

class TarefaBase(BaseModel):
    Aluno_ID: int
    Descricao: constr(max_length=100)
    Data_Prazo: datetime.date
    Completada: int
       
class TarefaInDB(TarefaBase):
    ID: int

    class Config:
        from_attributes = True
