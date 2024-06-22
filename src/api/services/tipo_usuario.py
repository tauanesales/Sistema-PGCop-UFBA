from typing import Optional, Union

from fastapi.security import OAuth2PasswordBearer
from loguru import logger
from passlib.context import CryptContext

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.services.aluno import ServicoAluno
from src.api.services.auth import ServicoAuth
from src.api.services.professor import ServiceProfessor
from src.api.services.servico_base import ServicoBase
from src.api.services.usuario import ServicoUsuario
from src.api.utils.enums import TipoUsuarioEnum

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoTipoUsuario(ServicoBase):
    _repo: PGCopRepository

    user_service_map = {
        TipoUsuarioEnum.COORDENADOR: ServiceProfessor,
        TipoUsuarioEnum.PROFESSOR: ServiceProfessor,
        TipoUsuarioEnum.ALUNO: ServicoAluno,
    }

    async def buscar_dados_por_tipo(self, usuario: Usuario) -> Union[Aluno, Professor]:
        tipo_usuario_service: ServicoBase = self.user_service_map[
            usuario.tipo_usuario.titulo
        ]
        logger.info(
            f"Buscando dados do usuário com base no tipo {usuario.tipo_usuario.titulo}."
        )
        return await tipo_usuario_service(self._repo).buscar_por_email(usuario.email)

    async def buscar_usuario_atual(
        self, token: str, tipo_usuario: Optional[TipoUsuarioEnum] = None
    ) -> Union[Aluno, Professor]:
        """Obtém o usuário atual com base no token fornecido."""
        logger.info("Obtendo usuário atual com base no token fornecido.")
        email = await ServicoAuth(self._repo).verificar_token(token)
        logger.info("Token verificado com sucesso.")
        usuario: Usuario = await ServicoUsuario(self._repo).buscar_por_email(
            email=email
        )
        logger.info("Usuário encontrado com sucesso.")
        if not tipo_usuario:
            return await self.buscar_dados_por_tipo(usuario=usuario)
        return await self.user_service_map[tipo_usuario](self._repo).buscar_por_email(
            email=email
        )
