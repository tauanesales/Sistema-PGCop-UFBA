from pydantic import BaseModel, constr, PositiveInt, conint
from enum import Enum

class CursoEnum(str, Enum):
    M = "M"
    D = "D"

class Tarefa_base_Base(BaseModel):
    nome: constr(max_length=255)
    descricao: constr()
    prazo_em_meses: PositiveInt
    curso: CursoEnum
       
class Tarefa_base_InDB(Tarefa_base_Base):
    id: int

    class Config:
        from_attributes = True
