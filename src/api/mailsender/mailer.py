from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from src.api.config import Config

import logging


class Mailer(object):
    """
    Classe para envio de emails.
    """
    
    def __init__(self):
        self.__sg_client = SendGridAPIClient(Config.SENDGRID_CONFIG.API_KEY)
    
    def send_message(self, dest_email: str, subject: str, html_content: str):
        """
        Envia uma mensagem para o usuário.
        """
        if Config.TESTING: return  # TODO: Está aqui porque ainda não conseguimos mockar o SendGrid

        message = Mail(
            from_email=Config.SENDGRID_CONFIG.EMAIL,
            to_emails=dest_email,
            subject=subject,
            html_content=html_content
        )

        try:
            self.__sg_client.send(message)
        except Exception as exception:
            logging.error(f"MailerError: {exception}")
            raise exception
