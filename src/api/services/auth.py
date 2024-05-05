from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.api.config import Config
from src.api.services.professor import ServiceProfessor
from src.api.services.aluno import ServiceAluno
from src.api.database.session import get_db
from sqlalchemy.orm import Session

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ServiceAuth:
    @staticmethod
    def verificar_senha(senha_plana: str, senha_hashed: str) -> bool:
        """Verifica se uma senha plana corresponde à sua versão hasheada."""
        return pwd_context.verify(senha_plana, senha_hashed)

    @staticmethod
    def gerar_senha_hash(senha: str) -> str:
        """Gera um hash para uma senha."""
        return pwd_context.hash(senha)

    @staticmethod
    def criar_access_token(data: dict, tipo_usuario: Optional[str] = None, expires_delta: Optional[timedelta] = None) -> str:
        """Cria um JWT token como string, opcionalmente incluindo o tipo de usuário."""
        to_encode = data.copy()
        if tipo_usuario:
            to_encode.update({"type": tipo_usuario})
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Config.AUTH.SECRET_KEY, algorithm=Config.AUTH.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verificar_token(token: str, credentials_exception) -> str:
        """Verifica um token JWT e extrai o identificador do usuário."""
        try:
            payload = jwt.decode(token, Config.AUTH.SECRET_KEY, algorithms=[Config.AUTH.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return username

async def obter_usuario_atual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> dict:
    """Obtém o usuário atual com base no token fornecido."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = ServiceAuth.verificar_token(token, credentials_exception)
    usuario = ServiceProfessor.obter_professor_por_email(db, email=email) or ServiceAluno.obter_aluno_por_email(db, email=email)
    if usuario:
        return usuario
    else:
        raise credentials_exception
