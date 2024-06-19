from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.aluno import Aluno
from src.api.database.models.tarefa import Tarefa
from src.api.exceptions.http_service_exception import AlunoNaoEncontradoException
from src.api.entrypoints.tarefas.errors import (
    ExcecaoGenerica,
    ExcecaoTarefaNaoEncontrada,
)
from src.api.entrypoints.tarefas.schema import TarefaBase
from src.api.services.aluno import ServicoAluno


class ServiceTarefa:
    @staticmethod
    async def validar_tarefa(db: AsyncSession, tarefa: TarefaBase):
        await ServicoAluno.obter_aluno(db, tarefa.aluno_id)

    @staticmethod
    async def criar_tarefa(db: AsyncSession, tarefa: TarefaBase):
        await ServiceTarefa.validar_tarefa(db=db, tarefa=tarefa)

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
    async def atualizar_tarefa(db: AsyncSession, tarefa_id: int, tarefa: TarefaBase):
        await ServiceTarefa.validar_tarefa(db=db, tarefa=tarefa)

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
    async def deletar_tarefa(db: AsyncSession, id: int):
        db.delete(ServiceTarefa.obter_tarefa(db, id))
        db.commit()

    @staticmethod
    async def obter_tarefa(db: AsyncSession, id: int):
        db_tarefa = db.query(Tarefa).filter(Tarefa.id == id).one_or_none()
        if not db_tarefa:
            raise ExcecaoTarefaNaoEncontrada()
        return db_tarefa

    @staticmethod
    async def obter_tarefas_por_aluno(db: AsyncSession, aluno_id: int):
        db_aluno = db.query(Tarefa).filter(Tarefa.aluno_id == aluno_id).all()
        if db_aluno is None:
            raise ExcecaoTarefaNaoEncontrada()
        return db_aluno
