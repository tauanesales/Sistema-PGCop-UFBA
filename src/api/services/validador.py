from typing import Optional

from loguru import logger

from src.api.database.models.professor import Professor
from src.api.entrypoints.professores.errors import ProfessorNaoEncontradoException
from src.api.entrypoints.professores.schema import ProfessorUpdate
from src.api.exceptions.http_service_exception import (
    DeveSeSubmeterPeloMenosUmCampoParaAtualizarException,
    TipoUsuarioInvalidoException,
)
from src.api.utils.enums import TipoUsuarioEnum


class ServicoValidador:
    @staticmethod
    def validar_professor_existe(db_professor: Optional[Professor]):
        if db_professor is None:
            raise ProfessorNaoEncontradoException()

    @staticmethod
    def validar_campos_de_atualizacao_nao_sao_nulos(updates_professor: ProfessorUpdate):
        if not any(updates_professor.model_dump().values()):
            raise DeveSeSubmeterPeloMenosUmCampoParaAtualizarException()

    @staticmethod
    def validar_tipo_usuario(
        updates_professor: ProfessorUpdate, *tipos_permitidos: list[TipoUsuarioEnum]
    ):
        if (
            updates_professor.tipo_usuario
            and updates_professor.tipo_usuario not in tipos_permitidos
        ):
            raise TipoUsuarioInvalidoException()

    @staticmethod
    def validar_atualizacao_de_professor(
        professor_id: int, updates_professor: ProfessorUpdate, db_professor: Professor
    ):
        ServicoValidador.validar_campos_de_atualizacao_nao_sao_nulos(updates_professor)
        logger.info(f"{professor_id=} | Existem campos não nulos para atualizar.")
        ServicoValidador.validar_professor_existe(db_professor)
        logger.info(f"{professor_id=} | Professor encontrado no banco de dados.")
        ServicoValidador.validar_tipo_usuario(
            updates_professor, TipoUsuarioEnum.PROFESSOR, TipoUsuarioEnum.COORDENADOR
        )
        logger.info(f"{professor_id=} | Tipo usuário válido.")
