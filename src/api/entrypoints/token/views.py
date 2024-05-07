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


router = APIRouter()


@router.post("/", response_model=Token)
async def login_para_acessar_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    usuario = ServiceProfessor.obter_professor_por_email(db, email=form_data.username)
    if not usuario or not ServiceAuth.verificar_senha(
        form_data.password, usuario.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = ServiceAuth.criar_access_token(
        data={"sub": usuario.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
