from datetime import datetime, timedelta
from enum import Enum

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.config import Config
from src.api.database.session import get_db
from src.api.entrypoints.alunos.errors import StudentNotFoundException
from src.api.entrypoints.professores.errors import ProfessorNotFoundException
from src.api.entrypoints.token.schema import Token
from src.api.exceptions.credentials_exception import CredentialsException
from src.api.services.aluno import ServiceAluno
from src.api.services.auth import ServiceAuth
from src.api.services.professor import ServiceProfessor

router = APIRouter()


class UserType(Enum):
    PROFESSOR = "professor"
    ALUNO = "aluno"


def authenticate_user(db: Session, email: str, password: str):
    try:
        user = ServiceProfessor.obter_por_email(db, email)
        if ServiceAuth.verificar_senha(password, user.senha_hash):
            return user, UserType.PROFESSOR
    except ProfessorNotFoundException:
        pass

    try:
        user = ServiceAluno.obter_por_email(db, email)
        if user and ServiceAuth.verificar_senha(password, user.senha_hash):
            return user, UserType.ALUNO
    except StudentNotFoundException:
        pass

    raise CredentialsException()


@router.post("/", response_model=Token)
async def login_para_acessar_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
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
