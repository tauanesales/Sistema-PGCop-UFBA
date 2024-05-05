from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.api.config import Config
from src.api.database.session import get_db
from src.api.services.auth import ServiceAuth
from src.api.services.professor import ServiceProfessor
from src.api.services.aluno import ServiceAluno
from src.api.entrypoints.token.schema import Token
from sqlalchemy.orm import Session
from enum import Enum

router = APIRouter()

class UserType(Enum):
    PROFESSOR = "professor"
    ALUNO = "aluno"

def authenticate_user(db: Session, email: str, password: str):
    user = ServiceProfessor.obter_por_email(db, email)
    print('B'*100)
    if user and ServiceAuth.verificar_senha(password, user.senha_hash):
        return user, UserType.PROFESSOR
    print('C'*100)
    user = ServiceAluno.obter_por_email(db, email)
    if user and ServiceAuth.verificar_senha(password, user.senha_hash):
        return user, UserType.ALUNO
    print('D'*100)

    return None, None

@router.post("/", response_model=Token)
async def login_para_acessar_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    print('A'*100)
    usuario, tipo_usuario = authenticate_user(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = ServiceAuth.criar_access_token(
        data={"sub": usuario.email, "type": tipo_usuario.value},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
