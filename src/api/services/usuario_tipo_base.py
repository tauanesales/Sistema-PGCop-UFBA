from abc import abstractmethod

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.repository import PGCopRepository

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoBase:
    def __init__(self, repository):
        self._repo = repository

    def buscar_atual(self, token: str = Depends(oauth2_scheme)):
        pass

    def obter_por_email(self, email: str):
        pass
