from pydantic import BaseModel, EmailStr, constr, validator
from datetime import date
from typing import ClassVar, Literal, Optional
from pydantic_br import CPF
from src.api.database.models.aluno import Aluno


class AlunoBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    cpf: CPF
    email: EmailStr
    telefone: constr(strip_whitespace=True, min_length=10, max_length=11)
    matricula: constr(min_length=6, max_length=12) 
    orientador_id: Optional[int] = None
    curso: Literal["M", "D"]
    lattes: Optional[constr(min_length=2, max_length=100)]
    data_ingresso: date
    data_qualificacao: Optional[date] 
    data_defesa: Optional[date]

class AlunoCreate(AlunoBase):
    senha: constr(min_length=7)

    @validator("nome", "telefone", "matricula", "lattes", pre=True)
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


class AlunoInDB(AlunoBase):
    id: int

    class Config:
        from_attributes = True
