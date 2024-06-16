from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, constr, field_validator
from pydantic_br import CPF

from src.api.exceptions.validation_exception import (
    PasswordWithoutLowercaseError,
    PasswordWithoutNumberError,
    PasswordWithoutSpecialCharacterError,
    PasswordWithoutUppercaseError,
    PasswordWithSpacesError,
)


class AlunoBase(BaseModel):
    nome: constr(min_length=2, max_length=100) = Field(
        ..., description="Nome completo do aluno."
    )
    cpf: CPF = Field(..., description="CPF do aluno.")
    email: EmailStr = Field(..., description="Endereço de email do aluno.")
    telefone: constr(strip_whitespace=True, min_length=10, max_length=11) = Field(
        ..., description="Número de telefone do aluno."
    )
    matricula: constr(min_length=6, max_length=12) = Field(
        ..., description="Matrícula do aluno."
    )
    orientador_id: Optional[int] = Field(
        None, description="ID do orientador do aluno, se houver."
    )
    curso: Literal["M", "D"] = Field(
        ..., description="Curso do aluno, Mestrado (M) ou Doutorado (D)."
    )
    lattes: Optional[constr(min_length=2, max_length=100)] = Field(
        None, description="Link para o currículo Lattes do aluno."
    )
    data_ingresso: date = Field(..., description="Data de ingresso do aluno no curso.")
    data_qualificacao: Optional[date] = Field(
        None, description="Data de qualificação do aluno, se aplicável."
    )
    data_defesa: Optional[date] = Field(
        None, description="Data de defesa do aluno, se aplicável."
    )


class AlunoCreate(AlunoBase):
    senha: constr(min_length=8) = Field(..., description="Senha de acesso do aluno.")

    @field_validator("nome", "telefone", "matricula", "lattes", mode="before")
    def blank_string(cls, value):
        if (
            isinstance(value, str)
            and value.replace(" ", "").replace("\t", "").replace("\r", "") == ""
        ):
            raise ValueError("O campo não pode estar em branco")
        return value

    @field_validator("nome", mode="before")
    def validar_nome(cls, nome: str):
        if not nome.replace(" ", "").isalpha():
            raise ValueError("O nome não pode conter números ou símbolos")
        return nome

    @field_validator("senha")
    def validar_senha(cls, senha: str):
        if " " in senha:
            raise PasswordWithSpacesError()
        if not any(char.isdigit() for char in senha):
            raise PasswordWithoutNumberError()
        if not any(char.isupper() for char in senha):
            raise PasswordWithoutUppercaseError()
        if not any(char.islower() for char in senha):
            raise PasswordWithoutLowercaseError()
        if senha.isalnum():
            raise PasswordWithoutSpecialCharacterError()
        return senha


class AlunoInDB(AlunoBase):
    id: int = Field(..., description="ID único do aluno no sistema.")

    class ConfigDict:
        from_attributes = True
