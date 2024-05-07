from datetime import datetime, timedelta
from sqlalchemy import select, join, update
from typing import Callable, Optional

from src.api.database.models.aluno import Aluno
from src.api.database.models.tarefa import Tarefa
from src.api.mailsender.workers import MailerWorker
from src.api.database.session import session

import asyncio


class TaskMailerWorker(MailerWorker):
    """
    Classe responsável por notificar por email 
    os usuários sobre tarefas perto do prazo.
    """

    def __get_tasks_near_to_deadline(self):
        """
        Retorna as tarefas pendentes, próximas ao prazo de entrega.
        """
        deadline = datetime.now() + timedelta(days=30)  # Expires in 1 month
            
        query = (
            select(
                Aluno.id, 
                Aluno.nome, 
                Aluno.email, 
                Tarefa.id.label("tarefa_id"), 
                Tarefa.data_prazo, 
                Tarefa.nome.label("titulo")
            )
            .select_from(
                join(Aluno, Tarefa, Aluno.id == Tarefa.aluno_id)
            )
            .where(Tarefa.data_prazo <= deadline.date())
            .where(Tarefa.last_notified.is_(None))
        )
        return session().execute(query)
    
    async def start(self, stop_function: Optional[Callable] = None):
        while stop_function is None or not stop_function():
            for task in self.__get_tasks_near_to_deadline():
                subject = f"[AVISO PGCOP] - Tarefa Pendente"
                body = self.load_html("task_near_to_deadline", task.nome, task.titulo)

                self.send_message(task.email, subject, body)

                query = update(Tarefa).where(Tarefa.id == task.tarefa_id).values(last_notified=str(datetime.now().date()))
                
                current_session = session()
                current_session.execute(query)
                current_session.commit()

            await asyncio.sleep(60 * 60)