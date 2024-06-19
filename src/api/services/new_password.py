import random

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.usuario import Usuario
from src.api.entrypoints.new_password.errors import (
    AuthenticationException,
    EmailNotFoundException,
)
from src.api.entrypoints.new_password.schema import NewPasswordCodeAuth
from src.api.html_loader import load_html
from src.api.mailsender.mailer import Mailer
from src.api.services.usuario import ServiceUsuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mailer = Mailer()


def generate_token(length=10) -> str:
    charset = "".join([chr(i) for i in range(ord("A"), ord("Z") + 1)])
    charset += "1234567890"

    return "".join(random.choice(charset) for i in range(length))


class ServiceNewPassword:
    @staticmethod
    async def authenticate(db: AsyncSession, email: str, token: str) -> None:
        db_user: Usuario = await ServiceUsuario.obter_por_email(db, email)

        if not db_user:
            raise AuthenticationException()

        if db_user.new_password_token != token:
            raise AuthenticationException()

    @staticmethod
    async def create_token(db: AsyncSession, email: str) -> NewPasswordCodeAuth:
        db_user: Usuario = await ServiceUsuario.obter_por_email(db, email)

        if not db_user:
            raise EmailNotFoundException()

        token = generate_token(6)

        db_user.new_password_token = token
        db.commit()
        db.refresh(db_user)

        mailer.send_message(
            dest_email=email,
            subject="[PGCOP] Código de redefinição de senha",
            html_content=load_html(
                "new_password_token", name=db_user.nome, token=token
            ),
        )
        return NewPasswordCodeAuth(email=email, token=token)

    @staticmethod
    async def set_new_password(
        db: AsyncSession, email: str, new_password: str, token: str
    ) -> None:
        db_user: Usuario =await  ServiceUsuario.obter_por_email(db, email)

        if not db_user:
            raise EmailNotFoundException()

        if db_user.new_password_token != token:
            raise AuthenticationException()

        db_user.senha_hash = pwd_context.hash(new_password)
        db_user.new_password_token = None

        db.commit()
        db.refresh(db_user)
