from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.api.config import Config

import asyncio
import logging


class Mailer:
    def __init__(self):
        self.sg_client = SendGridAPIClient(Config.SENDGRID_CONFIG.API_KEY)
    
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


async def start_mailer():
    mailer = Mailer()

    while True:
        mailer.check()
        await asyncio.sleep(60 * 60)