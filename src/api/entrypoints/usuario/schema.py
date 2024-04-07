from pydantic import BaseModel, EmailStr

class UsuarioBase(BaseModel):
    Nome: str
    Email: EmailStr
    Role: str

class UsuarioCreate(UsuarioBase):
    Senha: str

class UsuarioInDB(UsuarioBase):
    UserID: int

    class Config:
        from_attributes = True
