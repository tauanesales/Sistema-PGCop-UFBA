from enum import Enum

from pydantic import BaseModel, PositiveInt, constr, field_validator


class CursoEnum(str, Enum):
    M = "M"
    D = "D"


class Tarefa_base_Base(BaseModel):
    nome: constr(min_length=2, max_length=255)
    descricao: constr()
    prazo_em_meses: PositiveInt
    curso: CursoEnum

    @field_validator("nome", mode="before")
    def blank_string(cls, value):
        if (
            isinstance(value, str)
            and value.replace(" ", "").replace("\t", "").replace("\r", "") == ""
        ):
            raise ValueError("O campo não pode estar em branco")
        return value


class Tarefa_base_InDB(Tarefa_base_Base):
    id: int

    class ConfigDict:
        from_attributes = True
