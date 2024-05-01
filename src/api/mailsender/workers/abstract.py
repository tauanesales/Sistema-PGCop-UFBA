from abc import ABC, abstractmethod
from typing import Callable, Optional
from src.api.mailsender.mailer import Mailer



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