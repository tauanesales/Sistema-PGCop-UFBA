from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from src.api.exceptions.credentials_exception import CredentialsException
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
        email = ServiceAuth.verificar_token(token)
        usuario = ServiceProfessor.obter_por_email(db, email=email) or ServiceAluno.obter_por_email(db, email=email)
        if usuario:
            return usuario
        raise CredentialsException
