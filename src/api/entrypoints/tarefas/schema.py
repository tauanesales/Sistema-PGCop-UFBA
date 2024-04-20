from pydantic import BaseModel,constr
from typing import Literal


class TarefaBase(BaseModel):
    Descricao: constr(min_length=2, max_length=100)
    ProfessorID: int
    
    
class TarefaInDB(TarefaBase):
    TarefaID: int

    class Config:
        from_attributes = True
