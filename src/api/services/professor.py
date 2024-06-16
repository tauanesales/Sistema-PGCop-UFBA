from typing import List

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.session import get_db
from src.api.entrypoints.professores.errors import (
    EmailAlreadyRegisteredException,
    ProfessorNotFoundException,
)
from src.api.entrypoints.professores.schema import (
    ProfessorBase,
    ProfessorCreate,
    ProfessorInDB,
)
from src.api.services.auth import ServiceAuth, oauth2_scheme

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceProfessor:
    def get_current_professor(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ) -> ProfessorInDB:
        email = ServiceAuth.verificar_token(token)
        professor = db.query(Professor).filter(Professor.email == email).first()
        if not professor:
            raise ProfessorNotFoundException()
        return ProfessorInDB(**professor.__dict__)

    @staticmethod
    def validar_professor(db: Session, professor: ProfessorBase) -> None:
        if (
            db.query(Professor).filter(Professor.email == professor.email).first()
            or db.query(Aluno).filter(Aluno.email == professor.email).first()
        ):
            raise EmailAlreadyRegisteredException()

    @staticmethod
    def criar_professor(db: Session, professor: ProfessorCreate) -> ProfessorInDB:
        ServiceProfessor.validar_professor(db, professor)
        db_professor = Professor(
            nome=professor.nome,
            email=professor.email,
            senha_hash=pwd_context.hash(professor.senha),
            role=professor.role,
        )
        db.add(db_professor)
        db.commit()
        db.refresh(db_professor)
        return ProfessorInDB(**db_professor.__dict__)

    @staticmethod
    def obter_professor(db: Session, professor_id: int) -> ProfessorInDB:
        db_professor = (
            db.query(Professor).filter(Professor.id == professor_id).one_or_none()
        )
        if db_professor is None:
            raise ProfessorNotFoundException()
        return ProfessorInDB(**db_professor.__dict__)

    def obter_professores(db: Session) -> List[ProfessorInDB]:
        db_professors = db.query(Professor).all()
        if db_professors is None:
            raise ProfessorNotFoundException()
        return [ProfessorInDB(**professor.__dict__) for professor in db_professors]

    @staticmethod
    def deletar_professor(db: Session, professor_id: int) -> None:
        db_professor = (
            db.query(Professor).filter(Professor.id == professor_id).one_or_none()
        )
        if not db_professor:
            raise ProfessorNotFoundException()

        db.delete(db_professor)
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
            raise ProfessorNotFoundException()
        for key, value in updates_professor.model_dump().items():
            setattr(db_professor, key, value)
        db.commit()
        db.refresh(db_professor)
        return ProfessorInDB(**db_professor.__dict__)

    @staticmethod
    def obter_por_email(db: Session, email: str) -> Professor:
        db_professor = (
            db.query(Professor).filter(Professor.email == email).one_or_none()
        )
        if db_professor is None:
            raise ProfessorNotFoundException()
        return db_professor
