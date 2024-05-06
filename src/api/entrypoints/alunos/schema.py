from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, constr, validator, Field
from pydantic_br import CPF

class AlunoBase(BaseModel):
    nome: constr(min_length=2, max_length=100) = Field(..., description="Nome completo do aluno.")
    cpf: CPF = Field(..., description="CPF do aluno.")
    email: EmailStr = Field(..., description="Endereço de email do aluno.")
    telefone: constr(strip_whitespace=True, min_length=10, max_length=11) = Field(..., description="Número de telefone do aluno.")
    matricula: constr(min_length=6, max_length=12) = Field(..., description="Matrícula do aluno.")
    orientador_id: Optional[int] = Field(None, description="ID do orientador do aluno, se houver.")
    curso: Literal["M", "D"] = Field(..., description="Curso do aluno, Mestrado (M) ou Doutorado (D).")
    lattes: Optional[constr(min_length=2, max_length=100)] = Field(None, description="Link para o currículo Lattes do aluno.")
    data_ingresso: date = Field(..., description="Data de ingresso do aluno no curso.")
    data_qualificacao: Optional[date] = Field(None, description="Data de qualificação do aluno, se aplicável.")
    data_defesa: Optional[date] = Field(None, description="Data de defesa do aluno, se aplicável.")

class AlunoCreate(AlunoBase):
    senha: constr(min_length=7) = Field(..., description="Senha de acesso do aluno.")

    @validator("senha")
    def validar_senha(cls, senha):
        if " " in senha:
            raise ValueError("A senha não pode conter espaços.")
        return senha

class AlunoInDB(AlunoBase):
    id: int = Field(..., description="ID único do aluno no sistema.")

    class Config:
        from_attributes = True
