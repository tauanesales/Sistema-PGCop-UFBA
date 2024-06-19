import random

from loguru import logger
from passlib.context import CryptContext

from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.new_password.errors import AuthenticationException
from src.api.entrypoints.new_password.schema import NovaSenhaCodigoAutenticacao
from src.api.html_loader import load_html
from src.api.mailsender.mailer import Mailer
from src.api.services.servico_base import ServicoBase
from src.api.services.usuario import ServicoUsuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
mailer = Mailer()


def generate_token(length=10) -> str:
    charset = "".join([chr(i) for i in range(ord("A"), ord("Z") + 1)])
    charset += "1234567890"

    return "".join(random.choice(charset) for i in range(length))


class ServicoNovaSenha(ServicoBase):
    _repo: PGCopRepository

    async def autenticar_usuario_com_token(self, email: str, token: str) -> None:
        db_usuario: Usuario = await ServicoUsuario(self._repo).buscar_por_email(email)

        self._validador.validar_usuario_autenticado_por_usuario(db_usuario)
        self._validador.validar_usuari_autenticado_por_token(db_usuario, token)

    async def create_token(self, email: str) -> NovaSenhaCodigoAutenticacao:
        logger.info(f"{email=} | Solicitado token de nova senha")
        db_usuario: Usuario = await ServicoUsuario(self._repo).buscar_por_email(email)
        logger.info(f"{db_usuario.id=} {email=} | Usuário encontrado")

        self._validador.validar_email_nao_encontrado(db_usuario)

        token = generate_token(6)

        db_usuario.token_nova_senha = token

        mailer.send_message(
            dest_email=email,
            subject="[PGCOP] Código de redefinição de senha",
            html_content=load_html(
                "new_password_token", name=db_usuario.nome, token=token
            ),
        )
        logger.info(f"{db_usuario.id=} {email=} | Token enviado por email")
        return NovaSenhaCodigoAutenticacao(email=email, token=token)

    async def atualizar_para_nova_senha(
        self, email: str, new_password: str, token: str
    ) -> None:
        db_usuario: Usuario = await ServicoUsuario(self._repo).buscar_por_email(email)

        self._validador.validar_email_nao_encontrado(db_usuario)

        if db_usuario.token_nova_senha != token:
            raise AuthenticationException()

        db_usuario.senha_hash = pwd_context.hash(new_password)
        db_usuario.token_nova_senha = None
