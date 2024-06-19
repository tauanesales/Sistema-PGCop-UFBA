from pydantic import BaseModel, EmailStr, Field, constr

from src.api.schemas.usuario import ValidadorDeSenhaUsuario


class NovaSenhaSolicitada(BaseModel):
    email: EmailStr = Field(..., description="Endereço de email do aluno.")


class NovaSenhaCodigoAutenticacao(NovaSenhaSolicitada):
    token: constr(min_length=4) = Field(..., description="Código de autenticação.")


class NovaSenhaAtualizada(NovaSenhaCodigoAutenticacao, ValidadorDeSenhaUsuario):
    pass
