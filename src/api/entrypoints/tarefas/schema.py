from datetime import date
from pydantic import BaseModel, constr, validator
from typing import Literal, Optional


class TarefaBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    descricao: constr(max_length=100)
    completada: int
    data_prazo: date
    aluno_id: int
    last_notified: Optional[date] = None
    data_conclusao: Optional[date] = None

    @validator("nome", pre=True)
    def blank_string(cls, value):
        if isinstance(value, str) and value.replace(" ", "").replace("\t", "").replace("\r", "") == "":
            raise ValueError("O campo não pode estar em branco")
        return value


class TarefaInDB(TarefaBase):
    id: int

    class Config:
        from_attributes = True
