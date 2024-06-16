from datetime import date
from typing import Optional

from pydantic import BaseModel, constr, field_validator


class TarefaBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    descricao: constr(max_length=100)
    completada: int
    data_prazo: date
    aluno_id: int
    last_notified: Optional[date] = None
    data_conclusao: Optional[date] = None

    @field_validator("nome", mode="before")
    def blank_string(cls, value):
        if (
            isinstance(value, str)
            and value.replace(" ", "").replace("\t", "").replace("\r", "") == ""
        ):
            raise ValueError("O campo não pode estar em branco")
        return value


class TarefaInDB(TarefaBase):
    id: int

    class Config:
        from_attributes = True
