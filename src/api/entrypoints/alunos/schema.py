from pydantic import BaseModel, EmailStr, constr
from typing import Literal
from pydantic_br import CPF


class AlunoBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    cpf: CPF
    email_ufba: EmailStr
    matricula: constr(min_length=6, max_length=6) #Não sei se números de matricula podem conter mais que 6 dígitos
    orientador_id: constr(min_length=8, max_length=8)
    curso: Literal["M", "D"]


class AlunoInDB(AlunoBase):
    AlunoID: int

    class Config:
        from_attributes = True
