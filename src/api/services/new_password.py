from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.api.entrypoints.alunos.errors import StudentNotFoundException
from src.api.entrypoints.professores.errors import ProfessorNotFoundException
from src.api.entrypoints.new_password.errors import AuthenticationException, EmailNotFoundException
from src.api.entrypoints.new_password.schema import NewPasswordCodeAuth
from src.api.services.aluno import ServiceAluno
from src.api.services.professor import ServiceProfessor
from src.api.database.models.professor import Professor
from src.api.database.models.aluno import Aluno
from src.api.mailsender.mailer import Mailer

from typing import Optional, Union
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mailer = Mailer()


def generate_token(length = 10) -> str:
    charset = "".join([chr(i) for i in range(ord("A"), ord("Z") + 1)])
    charset += "1234567890"

    return "".join(random.choice(charset) for i in range(length))


class ServiceNewPassword:

    @staticmethod
    def __get_user_by_email(db: Session, email: str) -> Optional[Union[Aluno, Professor]]:
        user = None

        try: user = ServiceAluno.obter_por_email(db, email)
        except StudentNotFoundException: pass

        if not user:
            try: user = ServiceProfessor.obter_por_email(db, email)
            except ProfessorNotFoundException: pass

        return user

    @staticmethod
    def authenticate(db: Session, email: str, token: str) -> None:
        db_user = ServiceNewPassword.__get_user_by_email(db, email)

        if not db_user:
            raise AuthenticationException()
        
        if db_user.new_password_token != token:
            raise AuthenticationException()
    
    @staticmethod
    def create_token(db: Session, email: str) -> NewPasswordCodeAuth:
        db_user = ServiceNewPassword.__get_user_by_email(db, email)

        if not db_user:
            raise EmailNotFoundException()
        
        token = generate_token(6)

        db_user.new_password_token = token
        db.commit()
        db.refresh(db_user)

        mailer.send_message(
            dest_email=email, 
            subject="Seu código de confirmação chegou!",
            html_content=f"Olá, {db_user.nome}! <br>Este é o seu código: <b>{token}</b>"
        )
        return NewPasswordCodeAuth(email=email, token=token)

    @staticmethod
    def set_new_password(db: Session, email: str, new_password: str, token: str) -> None:
        db_user = ServiceNewPassword.__get_user_by_email(db, email)

        if not db_user:
            raise EmailNotFoundException()
        
        if db_user.new_password_token != token:
            raise AuthenticationException()
        
        db_user.senha_hash = pwd_context.hash(new_password)
        db_user.new_password_token = None

        db.commit()
        db.refresh(db_user)
