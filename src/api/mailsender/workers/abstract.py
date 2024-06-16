from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from src.api.mailsender.mailer import Mailer


__all__ = ["MailerWorker",]


class MailerWorker(ABC, Mailer):
    """
    Classe abstrata para monitoramento e envio 
    automático e contínuo de emails.
    """
    
    @abstractmethod
    async def start(stop_function: Optional[Callable] = None):
        """
        Inicializa o worker para executar em loop.
        """
        raise NotImplementedError()