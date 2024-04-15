from sqlalchemy.orm import Session

from src.api.database.models.aluno import Aluno
from src.api.entrypoints.alunos.schema import AlunoBase


class ServiceAluno:
    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoBase):
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
        return db.query(Aluno).filter(Aluno.UserID == aluno_id).one_or_none()

    @staticmethod
    def deletar_aluno(db: Session, aluno_id: int):
        db_aluno = db.query(Aluno).filter(Aluno.UserID == aluno_id).one_or_none()
        if db_aluno:
            db.delete(db_aluno)
            db.commit()
            return True
        return False

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, update_data: dict):
        db.query(Aluno).filter(Aluno.UserID == aluno_id).update(update_data)
        db.commit()
        return db.query(Aluno).filter(Aluno.UserID == aluno_id).one_or_none()

    @staticmethod
    def obter_aluno_por_email(db: Session, email: str):
        return db.query(Aluno).filter(Aluno.Email == email).one_or_none()

    @staticmethod
    def obter_aluno_por_cpf(db: Session, cpf: str):
        return db.query(Aluno).filter(Aluno.Cpf == cpf).one_or_none()
