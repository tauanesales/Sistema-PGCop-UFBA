from datetime import datetime
from typing import List

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.professores.schema import (
    ProfessorCreate,
    ProfessorInDB,
    ProfessorUpdate,
)
from src.api.services.auth import ServiceAuth, oauth2_scheme
from src.api.services.usuario import ServiceUsuario
from src.api.services.usuario_tipo_base import ServicoBase
from src.api.services.validador import ServicoValidador

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceProfessor(ServicoBase):
    _repo: PGCopRepository

    def buscar_atual(db: AsyncSession, token: str = Depends(oauth2_scheme)) -> ProfessorInDB:
        email = ServiceAuth.verificar_token(token)
        professor: Professor = ServiceProfessor.obter_por_email(db, email)
        return ProfessorInDB(
            id=professor.id,
            nome=professor.usuario.nome,
            email=professor.usuario.email,
            tipo_usuario=professor.usuario.tipo_usuario.titulo,
            user_id=professor.usuario.id,
        )

    @staticmethod
    def criar(db: AsyncSession, novo_professor: ProfessorCreate) -> ProfessorInDB:
        db_usuario_professor: Usuario = ServiceUsuario.criar(db, novo_professor)
        logger.info(f"Criando professor {novo_professor.tipo_usuario}")
        db_professor = Professor(usuario=db_usuario_professor)
        db.add(db_professor)
        db.commit()
        db.refresh(db_usuario_professor)
        db.refresh(db_professor)
        logger.info("Professor criado com sucesso.")
        return ServiceProfessor.de_professor_para_professor_in_db(db_professor)

    async def de_professor_para_professor_in_db(professor: Professor) -> ProfessorInDB:
        usuario: Usuario = professor.usuario
        return ProfessorInDB(
            id=professor.id,
            nome=usuario.nome,
            email=usuario.email,
            tipo_usuario=(usuario.tipo_usuario).titulo,
            user_id=usuario.id,
        )

    async def obter_professor(self, professor_id: int) -> ProfessorInDB:
        db_professor = await self._repo.buscar_por_id(professor_id, Professor)
        ServicoValidador.validar_professor_existe(db_professor)
        return await ServiceProfessor.de_professor_para_professor_in_db(db_professor)

    async def obter_professores(db: AsyncSession) -> List[ProfessorInDB]:
        db_professores = await PGCopRepository.buscar_todos(db, Professor)

        logger.info(db_professores[0])
        logger.info(dir(db_professores[0]))
        return [
            ServiceProfessor.de_professor_para_professor_in_db(professor)
            for professor in db_professores
        ]

    @staticmethod
    async def deletar(db: AsyncSession, professor_id: int) -> None:
        professor: Professor =await  PGCopRepository.buscar_por_id(db, professor_id, Professor)
        ServicoValidador.validar_professor_existe(professor)
        professor.deleted_at = datetime.now()
        professor.usuario.deleted_at = datetime.now()
        solicitacoes: list[Solicitacao] = professor.solicitacoes or []
        for solicitacao in solicitacoes:
            solicitacao.deleted_at = datetime.now()
        db.commit()

    @staticmethod
    async def atualizar_professor(
        db: AsyncSession, professor_id: int, updates_professor: ProfessorUpdate
    ) -> ProfessorInDB:
        db_professor: Professor = await PGCopRepository.buscar_por_id(
            db, professor_id, Professor
        )
        logger.info(
            f"{professor_id=} | Iniciando verificações para atualizar professor."
        )
        await ServicoValidador.validar_atualizacao_de_professor(
            db, professor_id, updates_professor, db_professor
        )

        db_professor.usuario.nome = updates_professor.nome or db_professor.usuario.nome
        db_professor.usuario.email = (
            updates_professor.email or db_professor.usuario.email
        )
        db_professor.usuario.tipo_usuario_id = (
           await PGCopRepository.buscar_id_tipo_usuario_por_titulo(
                db, updates_professor.tipo_usuario
            )
            if updates_professor.tipo_usuario
            else db_professor.usuario.tipo_usuario_id
        )
        db_professor.usuario.senha_hash = (
            pwd_context.hash(updates_professor.senha)
            if updates_professor.senha
            else db_professor.usuario.senha_hash
        )

        db.commit()
        db.refresh(db_professor)
        logger.info(f"{professor_id=} | Professor atualizado com sucesso.")
        return ServiceProfessor.de_professor_para_professor_in_db(db_professor)

    @staticmethod
    async def obter_por_email(db: AsyncSession, email: str) -> Professor:
        db_professor = await  PGCopRepository.buscar_professor_por_email(db, email)
        ServicoValidador.validar_professor_existe(db_professor)
        return db_professor
