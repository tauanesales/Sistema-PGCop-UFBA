from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.api.config import Config


#  hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Instânciando o  OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    def criar_access_token(
        data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Cria um JWT token como string."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, Config.AUTH.SECRET_KEY, algorithm=Config.AUTH.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    def verificar_token(token: str, credentials_exception) -> str:
        """Verifica um token JWT e extrai o identificador do usuário."""
        try:
            payload = jwt.decode(
                token, Config.AUTH.SECRET_KEY, algorithms=[Config.AUTH.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        return username

    @staticmethod
    async def obter_usuario_atual(token: str = Depends(oauth2_scheme)) -> str:
        """Dependência que pode ser usada em rotas para obter o usuário atual."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return ServiceAuth.verificar_token(token, credentials_exception)
