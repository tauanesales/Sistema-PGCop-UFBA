from sqlalchemy.orm import Session

from src.api.database.models.tarefa import Tarefa
from src.api.entrypoints.tarefas.errors import ExcecaoTarefaNaoEncontrada
from src.api.entrypoints.tarefas.schema import TarefaBase


class ServiceTarefa:
    
    @staticmethod
    def criar_tarefa(db: Session, tarefa: TarefaBase):

        db_tarefa = Tarefa(
            aluno_id=tarefa.aluno_id,
            nome=tarefa.nome,
            descricao=tarefa.descricao,
            data_prazo=tarefa.data_prazo,
            completada=tarefa.completada                       
        )
        db.add(db_tarefa)
        db.commit()
        db.refresh(db_tarefa)

        return db_tarefa
    
    @staticmethod
    def atualizar_tarefa(db: Session, tarefa_id: int, update_data: dict):
        db.query(Tarefa).filter(Tarefa.ID == tarefa_id).update(update_data)
        db.commit()

        db_tarefa = db.query(Tarefa).filter(Tarefa.ID == tarefa_id).one()
        
        if db_tarefa is None:
           raise ExcecaoTarefaNaoEncontrada()

        return db_tarefa
    
    @staticmethod
    def deletar_tarefa(db: Session, tarefa_id: int):
        db_tarefa = db.query(Tarefa).filter(Tarefa.ID == tarefa_id).one_or_none()

        if db_tarefa:
            db.delete(db_tarefa)
            db.commit()
        else:
            raise ExcecaoTarefaNaoEncontrada()
    
    @staticmethod
    def obter_tarefa(db: Session, id: int):
        db_tarefa = db.query(Tarefa).filter(Tarefa.ID == id).one_or_none()

        if db_tarefa is None:
            raise ExcecaoTarefaNaoEncontrada()

        return db_tarefa
    
    @staticmethod
    def obter_tarefas_aluno(db: Session, aluno_id: int):
        db_tarefas = db.query(Tarefa).filter(Tarefa.Aluno_ID == aluno_id).all()

        if db_tarefas is None:
            raise ExcecaoTarefaNaoEncontrada()

        return db_tarefas