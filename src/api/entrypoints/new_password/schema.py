from pydantic import BaseModel, EmailStr, Field, constr


class NewPasswordRequest(BaseModel):
    email: EmailStr = Field(..., description="Endereço de email do aluno.")


class NewPasswordCodeAuth(NewPasswordRequest):
    token: constr(min_length=4) = Field(..., description="Código de autenticação.")


class NewPasswordChange(NewPasswordRequest):
    nova_senha: constr(min_length=7) = Field(..., description="Nova senha de acesso do usuário.")