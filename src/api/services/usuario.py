from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.schemas.usuario import UsuarioCreate, UsuarioInDB
from src.api.services.usuario_tipo_base import ServicoBase
from src.api.services.validador import ServicoValidador

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceUsuario(ServicoBase):
    @staticmethod
    async def obter_por_email(db: AsyncSession, email: str) -> Usuario:
        db_usuario = db.query(Usuario).filter(Usuario.email == email).one_or_none()
        ServicoValidador.validar_usuario_existe(db_usuario)
        return db_usuario

    @staticmethod
    async def obter_usuario_por_id(db: AsyncSession, id: int) -> UsuarioInDB:
        db_usuario = await PGCopRepository.buscar_usuario_por_id(db, id)
        ServicoValidador.validar_usuario_existe(db_usuario)
        return UsuarioInDB(**db_usuario.__dict__)

    @staticmethod
    async def criar(db: AsyncSession, novo_usuario: UsuarioCreate) -> Usuario:
        logger.info(f"Criando usuario {novo_usuario.tipo_usuario}")
        await ServicoValidador.validar_email_registrado(db, novo_usuario)
        db_usuario = Usuario(
            nome=novo_usuario.nome,
            email=novo_usuario.email,
            senha_hash=pwd_context.hash(novo_usuario.senha),
            tipo_usuario_id=await PGCopRepository.buscar_id_tipo_usuario_por_titulo(
                db, novo_usuario.tipo_usuario
            ),
        )
        db.add(db_usuario)
        return db_usuario
