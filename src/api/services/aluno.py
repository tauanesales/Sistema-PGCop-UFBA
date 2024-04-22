from sqlalchemy.orm import Session

from src.api.database.models.aluno import Aluno
from src.api.entrypoints.alunos.errors import CPFAlreadyRegisteredException, StudentNotFoundException
from src.api.entrypoints.alunos.schema import AlunoBase


class ServiceAluno:
    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoBase):

        # CPF must not be registered.
        try: 
            ServiceAluno.obter_aluno_por_cpf(db, cpf=aluno.Cpf)
            raise CPFAlreadyRegisteredException()
        except StudentNotFoundException:
            pass

        db_aluno = Aluno(
            Nome=aluno.Nome,
            Cpf=aluno.Cpf,
            Email=aluno.Email,
            Telefone=aluno.Telefone,
            Matricula=aluno.Matricula,
            ProfessorID=aluno.ProfessorID,
            Role=aluno.Role,
        )
        db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)

        return db_aluno

    @staticmethod
    def obter_aluno(db: Session, aluno_id: int):
        db_aluno = db.query(Aluno).filter(Aluno.UserID == aluno_id).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno

    @staticmethod
    def deletar_aluno(db: Session, aluno_id: int):
        db_aluno = db.query(Aluno).filter(Aluno.UserID == aluno_id).one_or_none()

        if db_aluno:
            db.delete(db_aluno)
            db.commit()
        else:
            raise StudentNotFoundException()

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, update_data: dict):
        db.query(Aluno).filter(Aluno.UserID == aluno_id).update(update_data)
        db.commit()

        db_aluno = db.query(Aluno).filter(Aluno.UserID == aluno_id).one()
        
        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno

    @staticmethod
    def obter_aluno_por_email(db: Session, email: str):
        db_aluno = db.query(Aluno).filter(Aluno.Email == email).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno

    @staticmethod
    def obter_aluno_por_cpf(db: Session, cpf: str):
        db_aluno = db.query(Aluno).filter(Aluno.Cpf == cpf).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno
