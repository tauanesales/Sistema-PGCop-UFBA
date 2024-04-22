from pydantic import BaseModel, EmailStr, constr, validator
from typing import Literal


class UsuarioBase(BaseModel):
    Nome: constr(min_length=2, max_length=100)
    Email: EmailStr
    Role: Literal["professor", "orientador", "coordenador"]


class UsuarioCreate(UsuarioBase):
    Senha: constr(min_length=7)

    @validator("Senha")
    def validar_senha(cls, senha):
        if " " in senha:
            raise ValueError("A senha não pode conter espaços")
        return senha


class UsuarioInDB(UsuarioBase):
    UserID: int

    class Config:
        from_attributes = True
