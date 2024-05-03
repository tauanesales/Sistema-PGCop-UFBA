from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.api.database.models.aluno import Aluno
from src.api.database.models.tarefa import Tarefa
from src.api.entrypoints.alunos.errors import CPFAlreadyRegisteredException, StudentNotFoundException
from src.api.entrypoints.alunos.schema import AlunoBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ServiceAluno:
    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoBase):

        # CPF must not be registered.
        try: 
            ServiceAluno.obter_aluno_por_cpf(db, cpf=aluno.cpf)
            raise CPFAlreadyRegisteredException()
        except StudentNotFoundException:
            pass

        db_aluno = Aluno(
            nome=aluno.nome,
            cpf=aluno.cpf,
            email=aluno.email,
            telefone=aluno.telefone,
            matricula=aluno.matricula,
            lattes=aluno.lattes,
            orientador_id=aluno.orientador_id,
            curso=aluno.curso,
            data_ingresso=aluno.data_ingresso,
            data_qualificacao=aluno.data_qualificacao,
            data_defesa=aluno.data_defesa,
            senha_hash=pwd_context.hash(aluno.senha),
        )

        db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)

        return db_aluno

    @staticmethod
    def obter_aluno(db: Session, aluno_id: int):
        db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno

    @staticmethod
    def deletar_aluno(db: Session, aluno_id: int):
        db_tarefas = db.query(Tarefa).filter(Tarefa.aluno_id == aluno_id).all()
        for tarefa in db_tarefas:
            db.delete(tarefa)
        db.commit()

        db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).one_or_none()

        if db_aluno:
            db.delete(db_aluno)
            db.commit()
        else:
            raise StudentNotFoundException()

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, update_data: dict):
        db.query(Aluno).filter(Aluno.id == aluno_id).update(update_data)
        db.commit()

        db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).one()
        
        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno

    @staticmethod
    def obter_aluno_por_email(db: Session, email: str):
        db_aluno = db.query(Aluno).filter(Aluno.email == email).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno

    @staticmethod
    def obter_aluno_por_cpf(db: Session, cpf: str):
        db_aluno = db.query(Aluno).filter(Aluno.cpf == cpf).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno


    @staticmethod
    def obter_alunos_por_orientador(db: Session, orientador_id: int):
        db_aluno = db.query(Aluno).filter(Aluno.orientador_id == orientador_id).all()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno
