from datetime import datetime, timedelta
from sqlalchemy import select, join, update
from typing import Callable, Optional

from src.api.database.models.aluno import Aluno
from src.api.database.models.tarefa import Tarefa
from src.api.mailsender.workers import MailerWorker
from src.api.database.session import session
from src.api.html_loader import load_html

import asyncio


class TaskMailerWorker(MailerWorker):
    """
    Classe responsável por notificar por email 
    os usuários sobre tarefas perto do prazo,
    ou tarefas atrasadas.
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
                Tarefa.descricao,
                Tarefa.nome.label("titulo")
            )
            .select_from(
                join(Aluno, Tarefa, Aluno.id == Tarefa.aluno_id)
            )
            .where(Tarefa.data_prazo <= deadline.date())
            .where(Tarefa.last_notified.is_(None))
        )
        return session().execute(query)
    
    def __get_tasks_past_to_deadline(self):
        """
        Retorna as tarefas pendentes, fora do prazo de entrega.
        """            
        query = (
            select(
                Aluno.id, 
                Aluno.nome, 
                Aluno.email, 
                Tarefa.id.label("tarefa_id"), 
                Tarefa.data_prazo, 
                Tarefa.descricao,
                Tarefa.nome.label("titulo")
            )
            .select_from(
                join(Aluno, Tarefa, Aluno.id == Tarefa.aluno_id)
            )
            .where(Tarefa.data_prazo < datetime.now())
            .where(Tarefa.last_notified <= Tarefa.data_prazo)
        )
        return session().execute(query)
    
    async def start(self, stop_function: Optional[Callable] = None):
        while stop_function is None or not stop_function():
            for task in self.__get_tasks_near_to_deadline():
                subject = f"[PGCOP] Temos um lembrete para você"

                body = load_html(
                    "task_near_to_deadline", 
                    name=task.nome, 
                    task_title=task.titulo,
                    task_description=task.descricao.replace("\n", " "),
                    task_deadline=task.data_prazo.strftime("%d.%.m.%Y")
                )

                self.send_message(task.email, subject, body)

                query = update(Tarefa).where(Tarefa.id == task.tarefa_id).values(last_notified=str(datetime.now().date()))
                
                current_session = session()
                current_session.execute(query)
                current_session.commit()

            for task in self.__get_tasks_past_to_deadline():
                subject = f"[AVISO PGCOP] Tarefa Atrasada - Fique atento aos prazos"

                body = load_html(
                    "task_past_to_deadline", 
                    name=task.nome, 
                    task_title=task.titulo,
                    task_description=task.descricao.replace("\n", " "),
                    task_deadline=task.data_prazo.strftime("%d.%.m.%Y")
                )

                self.send_message(task.email, subject, body)

                query = update(Tarefa).where(Tarefa.id == task.tarefa_id).values(last_notified=str(datetime.now().date()))
                
                current_session = session()
                current_session.execute(query)
                current_session.commit()

            await asyncio.sleep(60 * 60)