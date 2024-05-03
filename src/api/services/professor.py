from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.entrypoints.professores.errors import EmailAlreadyRegisteredException, UserNotFoundException
from src.api.entrypoints.professores.schema import ProfessorCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceProfessor:
    @staticmethod
    def criar_professor(db: Session, professor: ProfessorCreate):

        # Email must not be registered.
        try: 
            ServiceProfessor.obter_professor_por_email(db, email=professor.email)
            raise EmailAlreadyRegisteredException()
        except UserNotFoundException:
            pass

        db_professor = Professor(
            nome=professor.nome,
            email=professor.email,
            senha_hash=pwd_context.hash(professor.senha),
            role=professor.role,
        )
        db.add(db_professor)
        db.commit()
        db.refresh(db_professor)

        return db_professor

    @staticmethod
    def obter_professor(db: Session, professor_id: int):
        db_professor = db.query(Professor).filter(Professor.id == professor_id).one_or_none()

        if db_professor is None:
            raise UserNotFoundException()

        return db_professor

    @staticmethod
    def deletar_professor(db: Session, professor_id: int):
        db.query(Aluno).filter(Aluno.orientador_id == professor_id).update({"orientador_id": None})
        db.commit()

        db_professor = db.query(Professor).filter(Professor.id == professor_id).one_or_none()

        if db_professor:
            db.delete(db_professor)
            db.commit()
        else:   
            raise UserNotFoundException()

    @staticmethod
    def atualizar_professor(db: Session, professor_id: int, update_data: dict):
        db.query(Professor).filter(Professor.id == professor_id).update(update_data)
        db.commit()

        db_professor = db.query(Professor).filter(Professor.id == professor_id).one()

        if db_professor is None:
            raise UserNotFoundException()
            
        return db_professor

    @staticmethod
    def obter_professor_por_email(db: Session, email: str):
        db_professor = db.query(Professor).filter(Professor.email == email).one_or_none()

        if db_professor is None:
            raise UserNotFoundException()
            
        return db_professor
