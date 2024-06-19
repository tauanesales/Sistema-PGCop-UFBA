from typing import Optional

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession


from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.alunos.schema import AlunoAtualizado
from src.api.entrypoints.professores.errors import ProfessorNaoEncontradoException
from src.api.entrypoints.professores.schema import ProfessorUpdate
from src.api.exceptions.http_service_exception import (
    AlunoNaoEncontradoException,
    DeveSeSubmeterPeloMenosUmCampoParaAtualizarException,
    EmailJaRegistradoException,
    TipoUsuarioInvalidoException,
    UsuarioNaoEncontradoException,
    NumeroJaRegistradoException,
)
from src.api.schemas.usuario import UsuarioBase
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
        tipo_usuario: TipoUsuarioEnum, *tipos_permitidos: list[TipoUsuarioEnum]
    ):
        if tipo_usuario and tipo_usuario not in tipos_permitidos:
            raise TipoUsuarioInvalidoException()

    @staticmethod
    async def validar_email_nao_esta_em_uso(
        db: AsyncSession,
        email: str,
        id,
    ):
        if await PGCopRepository.buscar_usuario_por_email_excluindo_id(db, email, id):
            raise EmailJaRegistradoException()

    @staticmethod
    async def validar_atualizacao_de_professor(
        db: AsyncSession,
        professor_id: int,
        updates_professor: ProfessorUpdate,
        db_professor: Professor,
    ):
        ServicoValidador.validar_professor_existe(db_professor)
        logger.info(f"{professor_id=} | Professor encontrado no banco de dados.")
        ServicoValidador.validar_campos_de_atualizacao_nao_sao_nulos(updates_professor)
        logger.info(f"{professor_id=} | Existem campos não nulos para atualizar.")
        ServicoValidador.validar_tipo_usuario(
            updates_professor.tipo_usuario,
            TipoUsuarioEnum.PROFESSOR,
            TipoUsuarioEnum.COORDENADOR,
        )
        logger.info(f"{professor_id=} | Tipo usuário válido.")
        await ServicoValidador.validar_email_nao_esta_em_uso(
            db, db_professor.usuario.email, professor_id
        )
        logger.info(f"{professor_id=} | Email não está em uso.")

    @staticmethod
    async def validar_email_registrado(
        db: AsyncSession,
        usuario: UsuarioBase,
    ) -> None:
        if await PGCopRepository.buscar_usuario_por_email(db, usuario.email):
            raise EmailJaRegistradoException()

    @staticmethod
    def validar_usuario_existe(db_usuario: Optional[Usuario]):
        if db_usuario is None:
            raise UsuarioNaoEncontradoException()

    @staticmethod
    async def buscar_e_validar_outro_aluno_possui_telefone(
        db: AsyncSession,
        telefone: Optional[str],
        aluno_id: int,
    ):
        if not telefone:
            return
        if await PGCopRepository.buscar_aluno_por_telefone_excluindo_id(
            db, telefone, aluno_id
        ):
            raise NumeroJaRegistradoException()

    @staticmethod
    async def buscar_e_validar_professor_existe(db: AsyncSession, professor_id: int,):
        if not professor_id:
            return
        professor: Optional[Professor] = await PGCopRepository.buscar_por_id(
            db,
            professor_id,
            Professor,
        )
        ServicoValidador.validar_professor_existe(professor)

    @staticmethod
    def validar_aluno_existe(db_aluno: Optional[Aluno]):
        if db_aluno is None:
            raise AlunoNaoEncontradoException()

    @staticmethod
    async def validar_atualizacao_de_aluno(
        db: AsyncSession,
        aluno_id: int,
        aluno_atualizado: AlunoAtualizado,
        db_aluno: Aluno,
    ):
        ServicoValidador.validar_aluno_existe(db_aluno)
        await ServicoValidador.buscar_e_validar_outro_aluno_possui_telefone(
            db, aluno_atualizado.telefone, aluno_id
        )
        await ServicoValidador.buscar_e_validar_professor_existe(
            db, aluno_atualizado.orientador_id
        )
        await ServicoValidador.validar_email_nao_esta_em_uso(
            db, aluno_atualizado.email, aluno_id
        )
        ServicoValidador.validar_tipo_usuario(
            aluno_atualizado.tipo_usuario, TipoUsuarioEnum.ALUNO
        )
