from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.tarefas_base import TarefasBase
from src.api.entrypoints.tarefas_base.errors import ExcecaoTarefaNaoEncontrada
from src.api.entrypoints.tarefas_base.schema import Tarefa_base_Base


class ServiceTarefaBase:
    @staticmethod
    async def criar_tarefa_base(db: AsyncSession, tarefa: Tarefa_base_Base):
        db_tarefa = TarefasBase(
            nome=tarefa.nome,
            descricao=tarefa.descricao,
            prazo_em_meses=tarefa.prazo_em_meses,
            curso=tarefa.curso,
        )
        db.add(db_tarefa)
        db.commit()
        db.refresh(db_tarefa)

        return db_tarefa

    @staticmethod
    async def atualizar_tarefa_base(db: AsyncSession, tarefa_id: int, update_data: dict):
        db.query(TarefasBase).filter(TarefasBase.id == tarefa_id).update(update_data)
        db.commit()

        db_tarefa = db.query(TarefasBase).filter(TarefasBase.id == tarefa_id).one()
        if db_tarefa is None:
            raise ExcecaoTarefaNaoEncontrada()
        return db_tarefa

    @staticmethod
    async def deletar_tarefa_base(db: AsyncSession, tarefa_id: int):
        db_tarefa = (
            db.query(TarefasBase).filter(TarefasBase.id == tarefa_id).one_or_none()
        )
        if not db_tarefa:
            raise ExcecaoTarefaNaoEncontrada()
        db.delete(db_tarefa)
        db.commit()

    @staticmethod
    async def obter_tarefa_base(db: AsyncSession, id: int):
        db_tarefa = db.query(TarefasBase).filter(TarefasBase.id == id).one_or_none()
        if db_tarefa is None:
            raise ExcecaoTarefaNaoEncontrada()
        return db_tarefa

    @staticmethod
    async def obter_tarefas_base_por_curso(db: AsyncSession, curso: str):
        db_tarefas = db.query(TarefasBase).filter(TarefasBase.curso == curso).all()
        if db_tarefas is None:
            raise ExcecaoTarefaNaoEncontrada()
        return db_tarefas
