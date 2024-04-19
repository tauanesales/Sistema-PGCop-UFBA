from sqlalchemy.orm import Session

from src.api.database.models.tarefa import Tarefa
#from src.api.entrypoints.alunos.errors import CPFAlreadyRegisteredException, StudentNotFoundException
from src.api.entrypoints.tarefas.schema import TarefaBase


class ServiceTarefa:
    @staticmethod
    def obter_tarefa(db: Session, tarefa_id: int):
        db_tarefa = db.query(Tarefa).filter(Tarefa.TarefaID == tarefa_id).one_or_none()

        #if db_tarefa is None:
         #   raise StudentNotFoundException()

        return db_tarefa