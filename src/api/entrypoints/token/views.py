from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.config import Config
from src.api.database.models.usuario import Usuario
from src.api.database.session import get_db
from src.api.entrypoints.token.schema import Token
from src.api.exceptions.credentials_exception import CredentialsException
from src.api.services.auth import ServiceAuth
from src.api.services.usuario import ServiceUsuario

router = APIRouter()


def authenticate_user(db: Session, email: str, password: str):
    user: Usuario = ServiceUsuario.obter_por_email(db, email)
    if ServiceAuth.verificar_senha(password, user.senha_hash):
        return user, user.tipo_usuario.titulo
    raise CredentialsException()


@router.post("/", response_model=Token)
async def login_para_acessar_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    usuario, tipo_usuario = authenticate_user(
        db, form_data.username, form_data.password
    )
    access_token_expires = timedelta(minutes=Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = ServiceAuth.criar_access_token(
        data={"sub": usuario.email, "type": tipo_usuario.value},
        expires_delta=access_token_expires,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expiration_date=datetime.now() + access_token_expires,
    )
