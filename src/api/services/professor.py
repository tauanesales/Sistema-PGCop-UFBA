from datetime import datetime
from typing import List

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.professores.errors import ProfessorNaoEncontradoException
from src.api.entrypoints.professores.schema import (
    ProfessorBase,
    ProfessorCreate,
    ProfessorInDB,
)
from src.api.services.auth import ServiceAuth, oauth2_scheme
from src.api.services.usuario import ServiceUsuario
from src.api.services.usuario_tipo_base import ServicoBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceProfessor(ServicoBase):
    def buscar_atual(db: Session, token: str = Depends(oauth2_scheme)) -> ProfessorInDB:
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
    def criar(db: Session, novo_professor: ProfessorCreate) -> ProfessorInDB:
        db_usuario_professor: Usuario = ServiceUsuario.criar(db, novo_professor)
        logger.info(f"Criando professor {novo_professor.tipo_usuario}")
        db_professor = Professor(usuario=db_usuario_professor)
        db.add(db_professor)
        db.commit()
        db.refresh(db_usuario_professor)
        db.refresh(db_professor)
        logger.info("Professor criado com sucesso.")
        return ServiceProfessor.de_professor_para_professor_in_db(db_professor)

    def de_professor_para_professor_in_db(professor: Professor) -> ProfessorInDB:
        return ProfessorInDB(
            id=professor.id,
            nome=professor.usuario.nome,
            email=professor.usuario.email,
            tipo_usuario=professor.usuario.tipo_usuario.titulo,
            user_id=professor.usuario.id,
        )

    @staticmethod
    def obter_professor(db: Session, professor_id: int) -> ProfessorInDB:
        db_professor = PGCopRepository.obter_por_id(db, professor_id, Professor)
        if db_professor is None:
            raise ProfessorNaoEncontradoException()
        return ServiceProfessor.de_professor_para_professor_in_db(db_professor)

    def obter_professores(db: Session) -> List[ProfessorInDB]:
        db_professors = PGCopRepository.obter_todos(db, Professor)
        if db_professors is None:
            raise ProfessorNaoEncontradoException()
        return [
            ServiceProfessor.de_professor_para_professor_in_db(professor)
            for professor in db_professors
        ]

    @staticmethod
    def deletar(db: Session, professor_id: int) -> None:
        professor: Professor = PGCopRepository.obter_por_id(db, professor_id, Professor)
        if not professor:
            raise ProfessorNaoEncontradoException()
        professor.deleted_at = datetime.now()
        professor.usuario.deleted_at = datetime.now()
        solicitacoes: list[Solicitacao] = professor.solicitacoes or []
        for solicitacao in solicitacoes:
            solicitacao.deleted_at = datetime.now()
        db.commit()

    @staticmethod
    def atualizar_professor(
        db: Session, professor_id: int, updates_professor: ProfessorBase
    ) -> ProfessorInDB:
        ServiceProfessor.validar_professor(db, updates_professor)
        db_professor = (
            db.query(Professor).filter(Professor.id == professor_id).one_or_none()
        )
        if db_professor is None:
            raise ProfessorNaoEncontradoException()
        for key, value in updates_professor.model_dump().items():
            setattr(db_professor, key, value)
        db.commit()
        db.refresh(db_professor)
        return ProfessorInDB(**db_professor.__dict__)

    @staticmethod
    def obter_por_email(db: Session, email: str) -> Professor:
        db_professor = PGCopRepository.obter_professor_por_email(db, email)
        if db_professor is None:
            raise ProfessorNaoEncontradoException()
        return db_professor
