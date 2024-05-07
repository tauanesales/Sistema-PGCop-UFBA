from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.entrypoints.alunos.errors import StudentNotFoundException
from src.api.entrypoints.professores.errors import EmailAlreadyRegisteredException, ProfessorNotFoundException
from src.api.entrypoints.professores.schema import ProfessorBase, ProfessorCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceProfessor:

    @staticmethod
    def validar_professor(db: Session, professor: ProfessorBase):
        try: 
            ServiceProfessor.obter_aluno_por_email(db, email=professor.email)
            raise EmailAlreadyRegisteredException()
        except StudentNotFoundException:
            pass

        try: 
            ServiceProfessor.obter_professor_por_email(db, email=professor.email)
            raise EmailAlreadyRegisteredException()
        except ProfessorNotFoundException:
            pass
        
    @staticmethod
    def validar_professor_update(db: Session, professor: ProfessorBase, professor_id:int):
        try: 
            aux_aluno = ServiceProfessor.obter_aluno_por_email(db, email=professor.email)
            if aux_aluno.id != professor_id:
                raise EmailAlreadyRegisteredException()
        except StudentNotFoundException:
            pass

        try: 
            aux_professor = ServiceProfessor.obter_professor_por_email(db, email=professor.email)
            if aux_professor.id != professor_id:
                raise EmailAlreadyRegisteredException()
        except ProfessorNotFoundException:
            pass


    @staticmethod
    def criar_professor(db: Session, professor: ProfessorCreate):

        ServiceProfessor.validar_professor(db=db, professor=professor)

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
            raise ProfessorNotFoundException()

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
            raise ProfessorNotFoundException()

    @staticmethod
    def atualizar_professor(db: Session, professor_id: int, professor: ProfessorBase):

        ServiceProfessor.validar_professor_update(db=db, professor=professor, professor_id=professor_id)

        db.query(Professor).filter(Professor.id == professor_id).update(professor.dict())
        db.commit()

        db_professor = db.query(Professor).filter(Professor.id == professor_id).one()

        if db_professor is None:
            raise ProfessorNotFoundException()
            
        return db_professor

    @staticmethod
    def obter_professor_por_email(db: Session, email: str):
        db_professor = db.query(Professor).filter(Professor.email == email).one_or_none()

        if db_professor is None:
            raise ProfessorNotFoundException()
            
        return db_professor
    
    @staticmethod
    def obter_aluno_por_email(db: Session, email: str):
        db_aluno = db.query(Aluno).filter(Aluno.email == email).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno
    
    
