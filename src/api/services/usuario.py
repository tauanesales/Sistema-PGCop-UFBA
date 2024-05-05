from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.services.aluno import ServiceAluno
from src.api.services.auth import ServiceAuth
from src.api.services.professor import ServiceProfessor

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ServiceUsuario:
    def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> dict:
        """Obtém o usuário atual com base no token fornecido."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
        email = ServiceAuth.verificar_token(token, credentials_exception)
        usuario = ServiceProfessor.obter_por_email(db, email=email) or ServiceAluno.obter_por_email(db, email=email)
        if usuario:
            return usuario
        else:
            raise credentials_exception
