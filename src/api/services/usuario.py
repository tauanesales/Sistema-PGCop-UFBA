from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext

from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.schemas.usuario import UsuarioInDB, UsuarioNovo
from src.api.services.servico_base import ServicoBase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoUsuario(ServicoBase):
    _repo: PGCopRepository

    async def buscar_por_email(self, email: str) -> Usuario:
        db_usuario = await self._repo.buscar_usuario_por_email(email)
        self._validador.validar_usuario_existe(db_usuario)
        return db_usuario

    async def obter_usuario_por_id(self, id: int) -> UsuarioInDB:
        db_usuario = await self._repo.buscar_usuario_por_id(id)
        self._validador.validar_usuario_existe(db_usuario)
        return UsuarioInDB(**db_usuario.__dict__)

    async def criar(self, novo_usuario: UsuarioNovo) -> Usuario:
        logger.info(
            f"Início do processo de criação de usuario tipo {novo_usuario.tipo_usuario}"
        )
        await self._validador.validar_email_registrado(novo_usuario)
        db_usuario = Usuario(
            nome=novo_usuario.nome,
            email=novo_usuario.email,
            senha_hash=pwd_context.hash(novo_usuario.senha),
            tipo_usuario=await self._repo.buscar_tipo_usuario_por_titulo(
                novo_usuario.tipo_usuario
            ),
        )
        await self._repo.criar(db_usuario)
        logger.info(f"{db_usuario.id=} | Usuario criado com sucesso.")
        return db_usuario
