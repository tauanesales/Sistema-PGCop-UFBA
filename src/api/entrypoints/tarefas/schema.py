import datetime
from pydantic import BaseModel, constr


class TarefaBase(BaseModel):
    aluno_id: int
    nome: constr(max_length=100)
    descricao: constr(max_length=100)
    data_prazo: datetime.date
    completada: int
       

class TarefaInDB(TarefaBase):
    ID: int

    class Config:
        from_attributes = True
