from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.database.models.aluno import Aluno
from src.api.database.models.tarefa import Tarefa
from src.api.entrypoints.alunos.errors import AlunoNaoEncontradoException
from src.api.entrypoints.tarefas.errors import (
    ExcecaoGenerica,
    ExcecaoIdAlunoNaoEncontrado,
    ExcecaoTarefaNaoEncontrada,
)
from src.api.entrypoints.tarefas.schema import TarefaBase


class ServiceTarefa:
    @staticmethod
    def validar_tarefa(db: Session, tarefa: TarefaBase):
        try:
            ServiceTarefa.obter_aluno(db, aluno_id=tarefa.aluno_id)
        except AlunoNaoEncontradoException:
            raise ExcecaoIdAlunoNaoEncontrado()

    @staticmethod
    def criar_tarefa(db: Session, tarefa: TarefaBase):
        ServiceTarefa.validar_tarefa(db=db, tarefa=tarefa)

        db_tarefa = Tarefa(
            aluno_id=tarefa.aluno_id,
            nome=tarefa.nome,
            last_notified=tarefa.last_notified,
            data_conclusao=tarefa.data_conclusao,
            descricao=tarefa.descricao,
            data_prazo=tarefa.data_prazo,
            completada=tarefa.completada,
        )

        db.add(db_tarefa)
        db.commit()
        db.refresh(db_tarefa)
        return db_tarefa

    @staticmethod
    def atualizar_tarefa(db: Session, tarefa_id: int, tarefa: TarefaBase):
        ServiceTarefa.validar_tarefa(db=db, tarefa=tarefa)

        try:
            db.query(Tarefa).filter(Tarefa.id == tarefa_id).update(tarefa.model_dump())
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise ExcecaoGenerica()

        db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).one()
        if db_tarefa is None:
            raise ExcecaoTarefaNaoEncontrada()
        return db_tarefa

    @staticmethod
    def deletar_tarefa(db: Session, tarefa_id: int):
        db_tarefa = db.query(Tarefa).filter(Tarefa.id == tarefa_id).one_or_none()

        if not db_tarefa:
            raise ExcecaoTarefaNaoEncontrada()
        db.delete(db_tarefa)
        db.commit()

    @staticmethod
    def obter_tarefa(db: Session, id: int):
        db_tarefa = db.query(Tarefa).filter(Tarefa.id == id).one_or_none()
        if db_tarefa is None:
            raise ExcecaoTarefaNaoEncontrada()
        return db_tarefa

    @staticmethod
    def obter_tarefas_por_aluno(db: Session, aluno_id: int):
        db_aluno = db.query(Tarefa).filter(Tarefa.aluno_id == aluno_id).all()
        if db_aluno is None:
            raise ExcecaoTarefaNaoEncontrada()
        return db_aluno

    @staticmethod
    def obter_aluno(db: Session, aluno_id: int):
        db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).one_or_none()
        if db_aluno is None:
            raise AlunoNaoEncontradoException()
        return db_aluno
