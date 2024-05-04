from datetime import datetime
from sqlalchemy import select
from typing import Callable, Optional

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
            
        query = select(Tarefa).where(Tarefa.Prazo == deadline.date())  # TODO: Tem que obter o email do aluno na query.
        result = session.execute(query)

        return result.scalars().all()
    
    async def start(stop_function: Optional[Callable] = None):
        while stop_function is None or not stop_function:
            # TODO: Implement
            await asyncio.sleep(60 * 60)