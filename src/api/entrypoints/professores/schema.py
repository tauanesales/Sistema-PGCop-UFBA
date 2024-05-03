from pydantic import BaseModel, EmailStr, constr, validator
from typing import Literal


class ProfessorBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    email: EmailStr
    role: Literal["orientador", "coordenador"]


class ProfessorCreate(ProfessorBase):
    senha: constr(min_length=7)

    @validator("senha")
    def validar_senha(cls, senha):
        if " " in senha:
            raise ValueError("A senha não pode conter espaços")
        return senha


class ProfessorInDB(ProfessorBase):
    id: int

    class Config:
        from_attributes = True
