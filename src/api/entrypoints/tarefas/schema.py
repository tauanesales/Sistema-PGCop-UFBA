from datetime import date

from pydantic import BaseModel, constr, field_validator
from typing import Optional

from src.api.utils.decorators import partial_model


class TarefaBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    descricao: constr(max_length=100)
    data_prazo: date
    aluno_id: int
    concluida: bool
    data_conclusao: Optional[date] = None

    @field_validator("nome", mode="before")
    def blank_string(cls, value):
        if (
            isinstance(value, str)
            and value.replace(" ", "").replace("\t", "").replace("\r", "") == ""
        ):
            raise ValueError("O campo não pode estar em branco")
        return value

@partial_model
class TarefaAtualizada(TarefaBase):
   
    data_conclusao: Optional[date] = None  # Campo opcional para data de conclusão

class TarefaInDB(TarefaBase):
    id: int

    class ConfigDict:
        from_attributes = True

class TarefaUpdate(BaseModel):
    concluida: Optional[bool] = None
    data_conclusao: Optional[date] = None