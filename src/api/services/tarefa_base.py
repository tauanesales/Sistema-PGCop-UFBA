from enum import Enum
from sqlalchemy.orm import Session

from src.api.database.models.tarefa import Tarefa
from src.api.database.models.tarefas_base import TarefasBase
from src.api.entrypoints.tarefas_base.errors import ExcecaoTarefaNaoEncontrada
from src.api.entrypoints.tarefas_base.schema import Tarefa_base_Base


class ServiceTarefaBase:
    
    @staticmethod
    def criar_tarefa_base(db: Session, tarefa: Tarefa_base_Base):

        db_tarefa = TarefasBase(
            nome=tarefa.nome,
            descricao=tarefa.descricao,
            prazo_em_meses=tarefa.prazo_em_meses,
            curso=tarefa.curso                       
        )
        db.add(db_tarefa)
        db.commit()
        db.refresh(db_tarefa)

        return db_tarefa
    
    @staticmethod
    def atualizar_tarefa_base(db: Session, tarefa_id: int, update_data: dict):
        db.query(TarefasBase).filter(TarefasBase.id == tarefa_id).update(update_data)
        db.commit()

        db_tarefa = db.query(TarefasBase).filter(TarefasBase.id == tarefa_id).one()
        
        if db_tarefa is None:
           raise ExcecaoTarefaNaoEncontrada()

        return db_tarefa
    
    @staticmethod
    def deletar_tarefa_base(db: Session, tarefa_id: int):
        db_tarefa = db.query(TarefasBase).filter(TarefasBase.id == tarefa_id).one_or_none()

        if db_tarefa:
            db.delete(db_tarefa)
            db.commit()
        else:
            raise ExcecaoTarefaNaoEncontrada()
    
    @staticmethod
    def obter_tarefa_base(db: Session, id: int):
        db_tarefa = db.query(TarefasBase).filter(TarefasBase.id == id).one_or_none()

        if db_tarefa is None:
            raise ExcecaoTarefaNaoEncontrada()

        return db_tarefa
    
    @staticmethod
    def obter_tarefas_base_por_curso(db: Session, curso: str):
        db_tarefas = db.query(TarefasBase).filter(TarefasBase.curso == curso).all()

        if db_tarefas is None:
            raise ExcecaoTarefaNaoEncontrada()

        return db_tarefas