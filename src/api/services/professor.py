from datetime import datetime

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext

from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.professores.schema import (
    ProfessorAtualizado,
    ProfessorInDB,
    ProfessorNovo,
)
from src.api.services.auth import ServicoAuth, oauth2_scheme
from src.api.services.servico_base import ServicoBase
from src.api.services.usuario import ServicoUsuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceProfessor(ServicoBase):
    _repo: PGCopRepository

    async def buscar_atual(self, token: str = Depends(oauth2_scheme)) -> ProfessorInDB:
        email = await ServicoAuth(self._repo).verificar_token(token)
        professor: Professor = await self.buscar_por_email(email)
        return ProfessorInDB(
            id=professor.id,
            nome=professor.usuario.nome,
            email=professor.usuario.email,
            tipo_usuario=professor.usuario.tipo_usuario.titulo,
            usuario_id=professor.usuario.id,
        )

    async def criar(self, novo_professor: ProfessorNovo) -> ProfessorInDB:
        db_usuario_professor: Usuario = await ServicoUsuario(self._repo).criar(
            novo_professor
        )
        logger.info(f"Criando professor {novo_professor.tipo_usuario}")
        db_professor = Professor(usuario=db_usuario_professor)
        await self._repo.criar(db_professor)
        logger.info(f"{db_professor.id=} | Professor criado com sucesso.")
        return self.tipo_usuario_in_db(db_professor)

    def tipo_usuario_in_db(self, professor: Professor) -> ProfessorInDB:
        usuario: Usuario = professor.usuario
        return ProfessorInDB(
            id=professor.id,
            nome=usuario.nome,
            email=usuario.email,
            tipo_usuario=(usuario.tipo_usuario).titulo,
            usuario_id=usuario.id,
        )

    async def buscar_por_id(self, professor_id: int) -> Professor:
        db_professor: Professor = await self._repo.buscar_por_id(
            professor_id, Professor
        )
        self._validador.validar_professor_existe(db_professor)
        return db_professor

    async def buscar_dados_in_db_por_id(self, professor_id: int) -> ProfessorInDB:
        return self.tipo_usuario_in_db(await self.buscar_por_id(professor_id))

    async def obter_professores(self) -> list[ProfessorInDB]:
        db_professores: list[Professor] = await self._repo.buscar_todos(Professor)
        return [self.tipo_usuario_in_db(professor) for professor in db_professores]

    async def deletar(self, professor_id: int) -> None:
        professor: Professor = await self._repo.buscar_por_id(professor_id, Professor)
        self._validador.validar_professor_existe(professor)
        solicitacoes: list[Solicitacao] = professor.solicitacoes or []
        logger.info(f"{professor_id=} {professor.usuario.id=} | Deletando professor;")
        for solicitacao in solicitacoes:
            solicitacao.deleted_at = datetime.utcnow()
        professor.deleted_at = datetime.utcnow()
        professor.usuario.deleted_at = datetime.utcnow()
        logger.info(f"{professor_id=} {professor.usuario.id=} | Professor deletado.")

    async def atualizar_professor(
        self, professor_id: int, updates_professor: ProfessorAtualizado
    ) -> ProfessorInDB:
        db_professor: Professor = await self._repo.buscar_por_id(
            professor_id, Professor
        )
        logger.info(
            f"{professor_id=} | Iniciando verificações para atualizar professor."
        )
        await self._validador.validar_atualizacao_de_professor(
            professor_id, updates_professor, db_professor
        )

        db_professor.usuario.nome = updates_professor.nome or db_professor.usuario.nome
        db_professor.usuario.email = (
            updates_professor.email or db_professor.usuario.email
        )
        db_professor.usuario.tipo_usuario = (
            await self._repo.buscar_tipo_usuario_por_titulo(
                updates_professor.tipo_usuario
            )
            if updates_professor.tipo_usuario
            else db_professor.usuario.tipo_usuario_id
        )
        db_professor.usuario.senha_hash = (
            pwd_context.hash(updates_professor.senha)
            if updates_professor.senha
            else db_professor.usuario.senha_hash
        )

        self._repo._session.flush()
        self._repo._session.refresh(db_professor)
        logger.info(f"{professor_id=} | Professor atualizado com sucesso.")
        return self.tipo_usuario_in_db(db_professor)

    async def buscar_por_email(self, email: str) -> Professor:
        db_professor = await self._repo.buscar_professor_por_email(email)
        self._validador.validar_professor_existe(db_professor)
        return db_professor

    async def buscar_dados_in_db_por_email(self, email: str) -> ProfessorInDB:
        return self.tipo_usuario_in_db(await self.buscar_por_email(email))
