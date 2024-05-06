from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.api.exceptions.credentials_exception import CredentialsException
from src.api.config import Config

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
    def verificar_token(token: str) -> str:
        """Verifica um token JWT e extrai o identificador do usuário."""
        try:
            payload = jwt.decode(token, Config.AUTH.SECRET_KEY, algorithms=[Config.AUTH.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException()
        except JWTError:
            raise CredentialsException()
        return username
