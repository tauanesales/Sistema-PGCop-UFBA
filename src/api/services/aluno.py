from typing import List

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.tarefa import Tarefa
from src.api.database.session import get_db
from src.api.entrypoints.alunos.errors import (
    CPFAlreadyRegisteredException,
    EmailAlreadyRegisteredException,
    ExcecaoIdOrientadorNaoEncontrado,
    MatriculaAlreadyRegisteredException,
    StudentNotFoundException,
)
from src.api.entrypoints.alunos.schema import AlunoBase, AlunoCreate, AlunoInDB
from src.api.services.auth import ServiceAuth, oauth2_scheme

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceAluno:
    def get_current_aluno(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ) -> AlunoInDB:
        email = ServiceAuth.verificar_token(token)
        aluno = db.query(Aluno).filter(Aluno.email == email).first()
        if not aluno:
            raise StudentNotFoundException()
        return AlunoInDB(**aluno.__dict__)

    @staticmethod
    def validar_aluno(db: Session, aluno: AlunoBase) -> None:
        if db.query(Aluno).filter_by(cpf=aluno.cpf).first():
            raise CPFAlreadyRegisteredException()
        if (
            db.query(Aluno).filter_by(email=aluno.email).first()
            or db.query(Professor).filter_by(email=aluno.email).first()
        ):
            raise EmailAlreadyRegisteredException()
        if (
            aluno.orientador_id
            and not db.query(Professor).filter_by(id=aluno.orientador_id).first()
        ):
            raise ExcecaoIdOrientadorNaoEncontrado()
        if db.query(Aluno).filter_by(matricula=aluno.matricula).first():
            raise MatriculaAlreadyRegisteredException()

    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoCreate) -> AlunoInDB:
        ServiceAluno.validar_aluno(db, aluno)
        senha_hash = pwd_context.hash(aluno.senha)

        aluno_dict = aluno.model_dump()
        del aluno_dict["senha"]

        novo_aluno = Aluno(**aluno_dict, senha_hash=senha_hash)
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return AlunoInDB(**novo_aluno.__dict__)

    @staticmethod
    def obter_aluno(db: Session, aluno_id: int) -> AlunoInDB:
        aluno = db.query(Aluno).filter_by(id=aluno_id).one_or_none()
        if not aluno:
            raise StudentNotFoundException()
        return AlunoInDB(**aluno.__dict__)

    @staticmethod
    def atualizar_aluno(
        db: Session, aluno_id: int, updates_aluno: AlunoBase
    ) -> AlunoInDB:
        db_aluno = db.query(Aluno).filter_by(id=aluno_id).one_or_none()
        if not db_aluno:
            raise StudentNotFoundException()
        for key, value in updates_aluno.model_dump().items():
            setattr(db_aluno, key, value)
        db.commit()
        db.refresh(db_aluno)
        return AlunoInDB(**db_aluno.__dict__)

    @staticmethod
    def deletar_aluno(db: Session, aluno_id: int) -> None:
        tarefas = db.query(Tarefa).filter(Tarefa.aluno_id == aluno_id).all()
        for tarefa in tarefas:
            db.delete(tarefa)
        db.flush()

        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).one_or_none()
        if not aluno:
            raise StudentNotFoundException()
        db.delete(aluno)
        db.commit()

    @staticmethod
    def obter_alunos_por_orientador(db: Session, orientador_id: int) -> List[AlunoInDB]:
        alunos = db.query(Aluno).filter_by(orientador_id=orientador_id).all()
        if not alunos:
            raise StudentNotFoundException()
        return [AlunoInDB(**aluno.__dict__) for aluno in alunos]

    @staticmethod
    def obter_por_email(db: Session, email: str) -> Aluno:
        db_aluno = db.query(Aluno).filter(Aluno.email == email).one_or_none()
        if db_aluno is None:
            raise StudentNotFoundException()
        return db_aluno

    @staticmethod
    def obter_aluno_por_cpf(db: Session, cpf: str) -> AlunoInDB:
        db_aluno = db.query(Aluno).filter(Aluno.cpf == cpf).one_or_none()
        if db_aluno is None:
            raise StudentNotFoundException()
        return AlunoInDB(**db_aluno.__dict__)
