from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional, Literal
from enum import Enum

class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[int] = None  # Expiry timestamp

class Login(BaseModel):
    email: EmailStr
    senha: constr(min_length=8)  # Exigindo mínimo de 8 caracteres

    @validator('senha')
    def senha_strength(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError("Senha deve conter pelo menos um número")
        if not any(char.isupper() for char in value):
            raise ValueError("Senha deve conter pelo menos uma letra maiúscula")
        return value



















