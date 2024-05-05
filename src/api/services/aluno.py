from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from src.api.services.auth import verify_token, oauth2_scheme
from src.api.database.models.professor import Professor
from src.api.database.models.aluno import Aluno
from src.api.database.models.tarefa import Tarefa
from src.api.entrypoints.alunos.errors import (
    CPFAlreadyRegisteredException, StudentNotFoundException,
    EmailAlreadyRegisteredException, MatriculaAlreadyRegisteredException,
    ExcecaoIdOrientadorNaoEncontrado
)
from src.api.database.session import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ServiceAluno:

    def get_current_aluno(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Aluno:
        email = verify_token(token)
        aluno = db.query(Aluno).filter(Aluno.email == email).first()
        if not aluno:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
        return aluno

    @staticmethod
    def validar_aluno(db: Session, aluno):
        if db.query(Aluno).filter_by(cpf=aluno.cpf).first() or db.query(Aluno).filter_by(email=aluno.email).first():
            raise EmailAlreadyRegisteredException()
        if aluno.orientador_id and not db.query(Professor).filter_by(id=aluno.orientador_id).first():
            raise ExcecaoIdOrientadorNaoEncontrado()

    @staticmethod
    def criar_aluno(db: Session, aluno) -> Aluno:
        ServiceAluno.validar_aluno(db, aluno)
        senha_hash = pwd_context.hash(aluno.senha)
        novo_aluno = Aluno(**aluno.dict(), senha_hash=senha_hash)
        db.add(novo_aluno)
        db.commit()
        db.refresh(novo_aluno)
        return novo_aluno

    @staticmethod
    def obter_aluno(db: Session, aluno_id: int) -> Aluno:
        aluno = db.query(Aluno).filter_by(id=aluno_id).one_or_none()
        if not aluno:
            raise StudentNotFoundException()
        return aluno

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, updates) -> Aluno:
        aluno = db.query(Aluno).filter_by(id=aluno_id).one_or_none()
        if not aluno:
            raise StudentNotFoundException()
        for key, value in updates.items():
            setattr(aluno, key, value)
        db.commit()
        return aluno

    @staticmethod
    def deletar_aluno(db: Session, aluno_id: int):
        aluno = db.query(Aluno).filter_by(id=aluno_id).one_or_none()
        if not aluno:
            raise StudentNotFoundException()
        db.delete(aluno)
        db.commit()

    @staticmethod
    def obter_alunos_por_orientador(db: Session, orientador_id: int):
        alunos = db.query(Aluno).filter_by(orientador_id=orientador_id).all()
        if not alunos:
            raise StudentNotFoundException()
        return alunos
