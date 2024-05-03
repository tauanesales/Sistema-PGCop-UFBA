from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.context import CryptContext

from src.api.database.models.professor import Professor
from src.api.database.models.aluno import Aluno
from src.api.database.models.tarefa import Tarefa
from src.api.entrypoints.alunos.errors import CPFAlreadyRegisteredException, StudentNotFoundException,EmailAlreadyRegisteredException ,MatriculaAlreadyRegisteredException,ExcecaoIdOrientadorNaoEncontrado , ExcecaoGenerica
from src.api.entrypoints.alunos.schema import AlunoBase

from src.api.entrypoints.professores.errors import ProfessorNotFoundException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ServiceAluno:

    @staticmethod
    def validar_aluno(db: Session, aluno: AlunoBase):
        try: 
            ServiceAluno.obter_aluno_por_cpf(db, cpf=aluno.cpf)
            raise CPFAlreadyRegisteredException()
        except StudentNotFoundException:
            pass

        try: 
            ServiceAluno.obter_aluno_por_email(db, email=aluno.email)
            raise EmailAlreadyRegisteredException()
        except StudentNotFoundException:
            pass

        try: 
            ServiceAluno.obter_professor_por_email(db, email=aluno.email)
            raise EmailAlreadyRegisteredException()
        except ProfessorNotFoundException:
            pass

        try: 
            ServiceAluno.obter_aluno_por_matricula(db, matricula=aluno.matricula)
            raise MatriculaAlreadyRegisteredException()
        except StudentNotFoundException:
            pass
        
        try: 
            if aluno.orientador_id is not None:
                ServiceAluno.obter_professor(db, professor_id=aluno.orientador_id)
        except ProfessorNotFoundException:
            raise ExcecaoIdOrientadorNaoEncontrado()
        
    @staticmethod
    def validar_aluno_update(db: Session, aluno: AlunoBase, aluno_id:int):
        try: 
            aux_aluno = ServiceAluno.obter_aluno_por_cpf(db, cpf=aluno.cpf)
            if aux_aluno.id != aluno_id:
                raise CPFAlreadyRegisteredException()
        except StudentNotFoundException:
            pass
        

        try: 
            aux_aluno = ServiceAluno.obter_aluno_por_email(db, email=aluno.email)
            if aux_aluno.id != aluno_id:
                raise EmailAlreadyRegisteredException()
        except StudentNotFoundException:
            pass

        try: 
            ServiceAluno.obter_professor_por_email(db, email=aluno.email)
            raise EmailAlreadyRegisteredException()
        except ProfessorNotFoundException:
            pass

        try: 
            aux_aluno = ServiceAluno.obter_aluno_por_matricula(db, matricula=aluno.matricula)
            if aux_aluno.id != aluno_id:
                raise MatriculaAlreadyRegisteredException()
        except StudentNotFoundException:
            pass
        
        try: 
            if aluno.orientador_id is not None:
                ServiceAluno.obter_professor(db, professor_id=aluno.orientador_id)
        except ProfessorNotFoundException:
            raise ExcecaoIdOrientadorNaoEncontrado()
        
    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoBase):

        ServiceAluno.validar_aluno(db,aluno)

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
    def atualizar_aluno(db: Session, aluno_id: int, aluno: AlunoBase):

        ServiceAluno.validar_aluno_update(db,aluno=aluno,aluno_id=aluno_id)

        db.query(Aluno).filter(Aluno.id == aluno_id).update(aluno.dict())
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
    def obter_aluno_por_matricula(db: Session, matricula: str):
        db_aluno = db.query(Aluno).filter(Aluno.matricula == matricula).one_or_none()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno


    @staticmethod
    def obter_alunos_por_orientador(db: Session, orientador_id: int):
        db_aluno = db.query(Aluno).filter(Aluno.orientador_id == orientador_id).all()

        if db_aluno is None:
            raise StudentNotFoundException()

        return db_aluno
    
    @staticmethod
    def obter_professor_por_email(db: Session, email: str):
        db_professor = db.query(Professor).filter(Professor.email == email).one_or_none()

        if db_professor is None:
            raise ProfessorNotFoundException()
            
        return db_professor
    
    @staticmethod
    def obter_professor(db: Session, professor_id: int):
        db_professor = db.query(Professor).filter(Professor.id == professor_id).one_or_none()

        if db_professor is None:
            raise ProfessorNotFoundException()

        return db_professor
