from enum import Enum

from pydantic import BaseModel, PositiveInt, constr, field_validator

from src.api.utils.decorators import partial_model
from src.api.utils.enums import CursoAlunoEnum


class TarefaBaseBase(BaseModel):
    nome: constr(min_length=2, max_length=255)
    descricao: constr(max_length=255)
    prazo_em_meses: PositiveInt
    curso: CursoAlunoEnum

    @field_validator("nome", mode="before")
    def blank_string(cls, value):
        if (
            isinstance(value, str)
            and value.replace(" ", "").replace("\t", "").replace("\r", "") == ""
        ):
            raise ValueError("O campo não pode estar em branco")
        return value


@partial_model
class TarefaBaseAtualizada(TarefaBaseBase):
    pass


class TarefaBaseInDB(TarefaBaseBase):
    id: int

    class ConfigDict:
        from_attributes = True
