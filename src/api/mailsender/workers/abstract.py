from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from src.api.mailsender.mailer import Mailer

import os


__all__ = ["MailerWorker",]

template_path = os.path.join(os.path.dirname(__file__), "templates")


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
    
    def load_html(self, filename: str, *params: Any) -> str:
        """
        Retorna o conteúdo de um arquivo template HTML. 
        """
        if not filename.endswith(".html"):
            filename += ".html"
            
        with open(os.path.join(template_path, filename), encoding="UTF-8") as file:
            content = file.read()

        return content.format(*params)