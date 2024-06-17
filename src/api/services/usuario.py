from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.api.database.models.usuario import Usuario

# from src.api.database.session import get_db
# from src.api.exceptions.credentials_exception import CredentialsException
from src.api.database.repository import PGCopRepository
from src.api.exceptions.http_service_exception import (
    EmailJaRegistradoException,
    UsuarioNaoEncontradoException,
)
from src.api.schemas.usuario import UsuarioBase, UsuarioCreate, UsuarioInDB
from src.api.services.usuario_tipo_base import ServicoBase

# from src.api.services.aluno import ServiceAluno
# from src.api.services.auth import ServiceAuth
# from src.api.services.professor import ServiceProfessor

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceUsuario(ServicoBase):
    @staticmethod
    def obter_por_email(db: Session, email: str) -> Usuario:
        db_usuario = db.query(Usuario).filter(Usuario.email == email).one_or_none()
        if db_usuario is None:
            raise UsuarioNaoEncontradoException()
        return db_usuario

    @staticmethod
    def obter_usuario_por_id(db: Session, id: int) -> UsuarioInDB:
        db_usuario = PGCopRepository.obter_usuario_por_id(db, id)
        if not db_usuario:
            raise UsuarioNaoEncontradoException()
        return UsuarioInDB(**db_usuario.__dict__)

    @staticmethod
    def validar_email_registrado(db: Session, usuario: UsuarioBase) -> None:
        if PGCopRepository.obter_usuario_por_email(db, usuario.email):
            raise EmailJaRegistradoException()

    @staticmethod
    def criar(db: Session, novo_usuario: UsuarioCreate) -> Usuario:
        logger.info(f"Criando usuario {novo_usuario.tipo_usuario}")
        ServiceUsuario.validar_email_registrado(db, novo_usuario)
        db_usuario = Usuario(
            nome=novo_usuario.nome,
            email=novo_usuario.email,
            senha_hash=pwd_context.hash(novo_usuario.senha),
            tipo_usuario_id=PGCopRepository.obter_id_tipo_usuario_por_titulo(
                db, novo_usuario.tipo_usuario
            ),
        )
        db.add(db_usuario)
        return db_usuario
