from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, field_validator

from src.api.exceptions.value_error_validation_exception import (
    PasswordWithoutLowercaseError,
    PasswordWithoutNumberError,
    PasswordWithoutSpecialCharacterError,
    PasswordWithoutUppercaseError,
    PasswordWithSpacesError,
)


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class Token(BaseModel):
    access_token: str
    token_type: str
    expiration_date: datetime


class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[int] = None  # Expiry timestamp


class Login(BaseModel):
    email: EmailStr
    senha: constr(min_length=8)  # Exigindo mínimo de 8 caracteres

    @field_validator("senha")
    def senha_strength(cls, senha: str):
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
