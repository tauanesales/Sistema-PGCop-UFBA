from abc import abstractmethod

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Instanciando o OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoBase:
    @abstractmethod
    def buscar_atual(db: Session, token: str = Depends(oauth2_scheme)):
        pass

    @abstractmethod
    def obter_por_email(db: Session, email: str):
        pass
