from pydantic import BaseModel,constr
from typing import Literal


class TarefaBase(BaseModel):
    Descricao: constr
    Status: constr
    
    
class TarefaInDB(TarefaBase):
    TarefaID: int

    class Config:
        from_attributes = True
