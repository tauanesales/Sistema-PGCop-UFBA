from pydantic import BaseModel, EmailStr, Field, constr, field_validator

from src.api.exceptions.value_error_validation_exception import (
    PasswordWithoutLowercaseError,
    PasswordWithoutNumberError,
    PasswordWithoutSpecialCharacterError,
    PasswordWithoutUppercaseError,
    PasswordWithSpacesError,
)
from src.api.utils.decorators import partial_model
from src.api.utils.enums import TipoUsuarioEnum


class UsuarioBase(BaseModel):
    nome: constr(min_length=3, max_length=100) = Field(
        ..., description="Nome completo."
    )
    email: EmailStr = Field(..., description="Endereço de email do usuário.")
    tipo_usuario: TipoUsuarioEnum = Field(..., description="Tipo de usuário.")

    @field_validator("nome", mode="before")
    def validar_nome(cls, nome):
        if (
            isinstance(nome, str)
            and nome.replace(" ", "").replace("\t", "").replace("\r", "") == ""
        ):
            raise ValueError("O campo não pode estar em branco")

        if not nome.replace(" ", "").isalpha():
            raise ValueError("O nome não pode conter números ou símbolos")
        return nome


class ValidadorDeSenhaUsuario:
    senha: constr(min_length=8)

    @field_validator("senha")
    def validar_senha(cls, senha: str):
        """Valida a senha fornecida durante a criação de um novo Usuario."""
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


class UsuarioNovo(UsuarioBase, ValidadorDeSenhaUsuario):
    pass


@partial_model
class UsuarioAtualizado(UsuarioNovo):
    pass


class UsuarioInDB(UsuarioBase):
    id: int

    class ConfigDict:
        from_attributes = (
            True  # Utiliza o ORM mode para compatibilidade com o SQLAlchemy
        )
