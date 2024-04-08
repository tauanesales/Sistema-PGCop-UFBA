from datetime import datetime

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from sqlalchemy import select

from src.api.config import Config
from src.api.database.models.tarefa import Tarefa
from src.api.database.session import session

from typing import Callable, Optional

import asyncio
import logging


class Mailer:
    def __init__(self):
        self.sg_client = SendGridAPIClient(Config.SENDGRID_CONFIG.API_KEY)

    def __get_tasks_near_to_deadline():
        """
        Retorna as tarefas pendentes, próximas ao prazo de entrega.
        """
        deadline = datetime.now() + timedelta(days=30)  # Expires in 1 month
            
        query = select(Tarefa).where(Tarefa.prazo == deadline.date())  # TODO: Tem que obter o email do aluno na query.
        result = session.execute(query)

        return result.scalars().all()
    
    def __send_message(dest: str, subject: str, content: str):
        """
        Envia uma mensagem para o usuário.
        """
        message = Mail(
            from_email=Config.SENDGRID_CONFIG.EMAIL,
            to_emails=dest,
            subject=subject,
            html_content=content
        )

        try:
            response = self.sg_client.send(message)
        except Exception as exception:
            logging.error(f"MailerError: {exception.message}")

    def check(self):
        """
        Verifica se há mensagens há serem enviadas.
        """
        pass  # TODO: Implementar isso.


async def start_mailer(stop_function: Optional[Callable] = None):
    """
    Inicializa o worker.
    """
    mailer = Mailer()

    while stop_function is None or not stop_function():
        mailer.check()
        await asyncio.sleep(60 * 60)