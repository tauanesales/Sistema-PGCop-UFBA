from typing import Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.usuario import Usuario
from src.api.entrypoints.alunos.schema import AlunoInDB
from src.api.entrypoints.professores.schema import ProfessorInDB
from src.api.services.aluno import ServicoAluno
from src.api.services.auth import ServiceAuth
from src.api.services.professor import ServiceProfessor
from src.api.services.usuario import ServiceUsuario
from src.api.services.usuario_tipo_base import ServicoBase
from src.api.utils.enums import TipoUsuarioEnum

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoTipoUsuario:
    user_service_map = {
        TipoUsuarioEnum.COORDENADOR: ServiceProfessor,
        TipoUsuarioEnum.PROFESSOR: ServiceProfessor,
        TipoUsuarioEnum.ALUNO: ServicoAluno,
    }

    @staticmethod
    def buscar_dados_por_tipo(
        db: AsyncSession, usuario: Usuario, token: str = Depends(oauth2_scheme)
    ) -> Union[AlunoInDB, ProfessorInDB]:
        tipo_usuario_service: ServicoBase = ServicoTipoUsuario.user_service_map[
            usuario.tipo_usuario.titulo
        ]
        logger.info(
            f"Buscando dados do usuário com base no tipo {usuario.tipo_usuario.titulo}."
        )
        return tipo_usuario_service.buscar_atual(db=db, token=token)

    @staticmethod
    def obter_usuario_atual(
        db: AsyncSession, token: str = Depends(oauth2_scheme)
    ) -> Union[AlunoInDB, ProfessorInDB]:
        """Obtém o usuário atual com base no token fornecido."""
        logger.info("Obtendo usuário atual com base no token fornecido.")
        email = ServiceAuth.verificar_token(token)
        logger.info("Token verificado com sucesso.")
        usuario: Usuario = ServiceUsuario.obter_por_email(db=db, email=email)
        logger.info("Usuário encontrado com sucesso.")
        return ServicoTipoUsuario.buscar_dados_por_tipo(
            db=db, usuario=usuario, token=token
        )
