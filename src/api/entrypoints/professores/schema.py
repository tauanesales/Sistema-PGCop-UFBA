from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, constr, field_validator

from src.api.exceptions.validation_exception import (
    PasswordWithoutLowercaseError,
    PasswordWithoutNumberError,
    PasswordWithoutSpecialCharacterError,
    PasswordWithoutUppercaseError,
    PasswordWithSpacesError,
)


class ProfessorBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    email: EmailStr
    role: Literal["orientador", "coordenador"]


class ProfessorCreate(ProfessorBase):
    senha: constr(min_length=7)

    @field_validator("nome", mode="before")
    def blank_string(cls, value):
        if (
            isinstance(value, str)
            and value.replace(" ", "").replace("\t", "").replace("\r", "") == ""
        ):
            raise ValueError("O campo não pode estar em branco")
        return value

    @field_validator("nome", mode="before")
    def validar_nome(cls, nome):
        if not nome.replace(" ", "").isalpha():
            raise ValueError("O nome não pode conter números ou símbolos")
        return nome

    @field_validator("senha")
    def validar_senha(cls, senha: str):
        """Valida a senha fornecida durante a criação de um novo professor."""
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


class ProfessorInDB(ProfessorBase):
    id: int
    senha_hash: Optional[str] = None  # Ajuste opcional do hash da senha

    class Config:
        from_attributes = (
            True  # Utiliza o ORM mode para compatibilidade com o SQLAlchemy
        )
