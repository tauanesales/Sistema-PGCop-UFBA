from pydantic import BaseModel, EmailStr, constr, validator
from typing import Literal


class ProfessorBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    email: EmailStr
    role: Literal["orientador", "coordenador"]


class ProfessorCreate(ProfessorBase):
    senha: constr(min_length=7)

    @validator("nome", pre=True)
    def blank_string(cls, value):
        if isinstance(value, str) and value.replace(" ", "").replace("\t", "").replace("\r", "") == "":
            raise ValueError("O campo não pode estar em branco")
        return value
    
    @validator("nome", pre=True)
    def validar_nome(cls, nome):
        for char in nome:
            if char in "1234567890!@#$%&*()-=+\/|[]{}'\";:":
                raise ValueError("O nome não pode conter números ou símbolos")
        return nome

    @validator("senha")
    def validar_senha(cls, senha):
        if " " in senha:
            raise ValueError("A senha não pode conter espaços")
        return senha


class ProfessorInDB(ProfessorBase):
    id: int

    class Config:
        from_attributes = True
