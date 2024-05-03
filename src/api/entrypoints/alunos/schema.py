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
    lattes: constr(min_length=2, max_length=100)
    data_ingresso: date
    data_qualificacao: date 
    data_defesa: date

class AlunoCreate(AlunoBase):
    senha: constr(min_length=7)

    @validator("senha")
    def validar_senha(cls, senha):
        if " " in senha:
            raise ValueError("A senha não pode conter espaços")
        return senha


class AlunoInDB(AlunoBase):
    id: int

    class Config:
        from_attributes = True
