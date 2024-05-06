from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import orm
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from src.api.services.auth import ServiceAuth, oauth2_scheme
from src.api.database.session import get_db
from src.api.database.models.professor import Professor
from src.api.database.models.aluno import Aluno
from src.api.entrypoints.professores.errors import EmailAlreadyRegisteredException, ProfessorNotFoundException
from src.api.entrypoints.professores.schema import ProfessorBase, ProfessorCreate, ProfessorInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ServiceProfessor:

    def get_current_professor(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> ProfessorInDB:
        email = ServiceAuth.verificar_token(token)
        professor = db.query(Professor).filter(Professor.email == email).first()
        if not professor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professor não encontrado")
        return professor

    @staticmethod
    def validar_professor(db: Session, professor: ProfessorBase):
        if db.query(Professor).filter(Professor.email == professor.email).first() or \
           db.query(Aluno).filter(Aluno.email == professor.email).first():
            raise EmailAlreadyRegisteredException()

    @staticmethod
    def criar_professor(db: Session, professor: ProfessorCreate) -> Professor:
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
        return db_professor

    @staticmethod
    def obter_professor(db: Session, professor_id: int) -> Professor:
        db_professor = db.query(Professor).filter(Professor.id == professor_id).one_or_none()
        if db_professor is None:
            raise ProfessorNotFoundException()
        return db_professor
    
    def obter_professores(db: Session) -> List[Professor]:
        db_professor = db.query(Professor).all()
        if db_professor is None:
            raise ProfessorNotFoundException()
        
        else:
            # List to store modified dictionaries
            modified_professors = []

            # Iterate through each professor object
            for professor in db_professor:
                # Convert the professor object to a dictionary
                professor_dict = professor.__dict__
                # Remove the 'senha_hash' key if it exists
                if 'senha_hash' in professor_dict:
                    del professor_dict['senha_hash']
                
                # Append the modified dictionary to the list
                modified_professors.append(professor_dict)

            # Return the list of modified dictionaries
            return modified_professors

    @staticmethod
    def deletar_professor(db: Session, professor_id: int):
        db_professor = db.query(Professor).filter(Professor.id == professor_id).one_or_none()
        if db_professor:
            db.delete(db_professor)
            db.commit()
        else:
            raise ProfessorNotFoundException()

    @staticmethod
    def atualizar_professor(db: Session, professor_id: int, professor: ProfessorBase):
        ServiceProfessor.validar_professor(db, professor)
        db.query(Professor).filter(Professor.id == professor_id).update(professor.dict())
        db.commit()
        db_professor = db.query(Professor).filter(Professor.id == professor_id).one()
        if db_professor is None:
            raise ProfessorNotFoundException()
        return db_professor

    @staticmethod
    def obter_por_email(db: Session, email: str) -> Professor:
        db_professor = db.query(Professor).filter(Professor.email == email).one_or_none()
        if db_professor is None:
            raise ProfessorNotFoundException()
        return db_professor
