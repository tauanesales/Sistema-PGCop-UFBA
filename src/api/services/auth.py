from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.api.config import Config
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.token.schema import Token
from src.api.exceptions.credentials_exception import CredentialsException
from src.api.services.servico_base import ServicoBase
from src.api.services.usuario import ServicoUsuario

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoAuth(ServicoBase):
    _repo: PGCopRepository

    def verificar_senha(self, senha_plana: str, senha_hashed: str) -> bool:
        """Verifica se uma senha plana corresponde à sua versão hasheada."""
        return pwd_context.verify(senha_plana, senha_hashed)

    def gerar_senha_hash(self, senha: str) -> str:
        """Gera um hash para uma senha."""
        return pwd_context.hash(senha)

    def criar_access_token(
        self,
        data: dict,
        tipo_usuario: Optional[str] = None,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """Cria um JWT token como string, opcionalmente incluindo o tipo de usuário."""
        to_encode = data.copy()
        if tipo_usuario:
            to_encode.update({"type": tipo_usuario})
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, Config.AUTH.SECRET_KEY, algorithm=Config.AUTH.ALGORITHM
        )
        return encoded_jwt

    async def verificar_token(self, token: str) -> str:
        """Verifica um token JWT e extrai o identificador do usuário."""
        try:
            payload = jwt.decode(
                token, Config.AUTH.SECRET_KEY, algorithms=[Config.AUTH.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialsException()
        except JWTError:
            raise CredentialsException()
        return username

    async def autenticar_usuario(self, email: str, password: str) -> Usuario:
        usuario: Usuario = await ServicoUsuario(self._repo).buscar_por_email(email)
        if not self.verificar_senha(password, usuario.senha_hash):
            raise CredentialsException()
        return usuario

    async def login_para_acessar_token(self, email: str, senha: str):
        usuario: Usuario = await self.autenticar_usuario(email, senha)
        access_token_expires = timedelta(
            minutes=Config.AUTH.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self.criar_access_token(
            data={"sub": usuario.email, "type": usuario.tipo_usuario.titulo},
            expires_delta=access_token_expires,
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
            expiration_date=datetime.utcnow() + access_token_expires,
        )
