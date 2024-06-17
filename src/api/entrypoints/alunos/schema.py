from datetime import date
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl, constr, field_validator
from pydantic_br import CPF
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.api.exceptions.validation_exception import (
    MatriculaNotNumericError,
    PasswordWithoutLowercaseError,
    PasswordWithoutNumberError,
    PasswordWithoutSpecialCharacterError,
    PasswordWithoutUppercaseError,
    PasswordWithSpacesError,
    CursoNotValidError,
    OrientadorStatusNotValidError
)

PhoneNumber.phone_format = "NATIONAL"
PhoneNumber.default_region_code = "BR"
PhoneNumber.min_length = 10
PhoneNumber.max_length = 22


class AlunoBase(BaseModel):
    nome: constr(min_length=2, max_length=100) = Field(
        ..., description="Nome completo do aluno."
    )
    cpf: CPF = Field(..., description="CPF do aluno.")
    email: EmailStr = Field(..., description="Endereço de email do aluno.")
    telefone: PhoneNumber = Field(..., description="Número de telefone do aluno.")
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

    orientador_status: Literal['nao_respondido', 'aceito','recusado'] = Field(
        ..., description="Aceite do orientador, 'aceito', 'recusado' ou 'nao_respondido'."
    )

    @field_validator("nome", "telefone", "matricula", "lattes", mode="before")
    def blank_string(cls, value):
        value = value.replace("\t", "").replace("\r", "").replace("\n", "")
        if not value.replace(" ", ""):
            raise ValueError("O campo não pode estar em branco")
        return value

    @field_validator("nome", mode="before")
    def validar_nome(cls, nome: str):
        if not nome.replace(" ", "").isalpha():
            raise ValueError("O nome não pode conter números ou símbolos")
        return nome

    @field_validator("matricula", mode="after")
    def validar_matricula(cls, matricula: str):
        if not matricula.isnumeric():
            raise MatriculaNotNumericError()
        return matricula

    @field_validator("telefone", mode="before")
    def validate_telefone(cls, value):
        return (
            value.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
        )

    @field_validator("lattes")
    def validar_lattes(cls, lattes: str):
        HttpUrl(lattes)
        return lattes

class AlunoCreate(AlunoBase):
    senha: constr(min_length=8) = Field(..., description="Senha de acesso do aluno.")

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


class AlunoUpdate(BaseModel):
    telefone: PhoneNumber = Field(..., description="Número de telefone do aluno.")
    lattes: Optional[constr(min_length=2, max_length=100)] = Field(
        None, description="Link para o currículo Lattes do aluno."
    )
    orientador_id: Optional[int] = Field(
        None, description="ID do orientador do aluno, se houver."
    )
    data_qualificacao: Optional[date] = Field(
        None, description="Data de qualificação do aluno, se aplicável."
    )
    data_defesa: Optional[date] = Field(
        None, description="Data de defesa do aluno, se aplicável."
    )

    orientador_status: Literal['nao_respondido','aceito','recusado'] = Field(
        ..., description="Aceite do orientador, 'aceito', 'recusado' ou 'nao_respondido'."
    )

    @field_validator("telefone", mode="before")
    def blank_string(cls, value):
        return (
            value.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
        )

    @field_validator("lattes")
    def validar_lattes(cls, lattes: str):
        HttpUrl(lattes)
        return lattes