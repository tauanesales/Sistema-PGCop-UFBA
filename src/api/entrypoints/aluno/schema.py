from pydantic import BaseModel, EmailStr, constr
from typing import Literal
from pydantic_br import CPF

class AlunoBase(BaseModel):
    Nome: constr(min_length=2, max_length=100)
    Cpf: CPF
    Email: EmailStr
    Telefone: constr(strip_whitespace=True, min_length=10, max_length=11)
    Matricula: constr(min_length=6, max_length=6) #Não sei se números de matricula podem conter mais que 6 dígitos
    ProfessorID = constr(min_length=8, max_length=8)
    Role: Literal["mestrado", "doutorando"]

class AlunoInDB(AlunoBase):
    AlunoID: int

    class Config:
        from_attributes = True
