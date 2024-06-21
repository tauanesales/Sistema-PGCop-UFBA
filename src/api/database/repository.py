from typing import Optional

from loguru import logger
from sqlalchemy import and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.aluno import Aluno
from src.api.database.models.entity_model_base import EntityModelBase
from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.tarefa import Tarefa
from src.api.database.models.tipo_usuario import TipoUsuario
from src.api.database.models.usuario import Usuario
from src.api.utils.enums import StatusSolicitacaoEnum, TipoUsuarioEnum


class PGCopRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def buscar_por_id(
        self, id: int, model: EntityModelBase
    ) -> Optional[EntityModelBase]:
        query = select(model).where(
            and_(model.id == id, model.deleted_at == None)  # noqa: E711
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_todos(self, model: EntityModelBase) -> list[EntityModelBase]:
        query = select(model).where(model.deleted_at == None)  # noqa: E711
        result = await self._session.execute(query)
        return result.scalars().unique().all()

    async def filtrar(self, model: EntityModelBase, **kwargs) -> list[EntityModelBase]:
        query = select(model).filter_by(**kwargs)
        result = await self._session.execute(query)
        return result.scalars().unique().all()

    async def criar(self, model: EntityModelBase) -> EntityModelBase:
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model

    async def salvar(self, model: EntityModelBase = None) -> None:
        await self._session.flush()
        if model:
            await self._session.refresh(model)

    async def atualizar_por_id(self, id: int, model: EntityModelBase, **kwargs) -> None:
        query = update(model).where(model.id == id).values(**kwargs)
        await self._session.execute(query)
        await self._session.flush()
        logger.info(f"{model.__name__} {id=} atualizado com sucesso.")

    async def buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        query = select(Usuario).where(
            and_(
                Usuario.email == email,
                Usuario.deleted_at == None,  # noqa: E711
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_aluno_por_email(self, email: str) -> Optional[Aluno]:
        query = (
            select(Aluno)
            .join(Usuario, Usuario.id == Aluno.usuario_id)
            .where(
                and_(
                    Usuario.email == email,
                    Aluno.deleted_at == None,  # noqa: E711
                    Usuario.deleted_at == None,  # noqa: E711
                )
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_professor_por_email(self, email: str) -> Optional[Usuario]:
        query = (
            select(Professor)
            .join(Usuario, Usuario.id == Professor.usuario_id)
            .join(TipoUsuario, Usuario.tipo_usuario_id == TipoUsuario.id)
            .where(
                and_(
                    Usuario.email == email,
                    or_(
                        TipoUsuario.titulo == TipoUsuarioEnum.PROFESSOR,
                        TipoUsuario.titulo == TipoUsuarioEnum.COORDENADOR,
                    ),
                    Usuario.deleted_at == None,  # noqa: E711
                    Professor.deleted_at == None,  # noqa: E711
                ),
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_usuario_por_id(self, id: int) -> Optional[Usuario]:
        return await self.buscar_por_id(id, Usuario)

    async def buscar_tipo_usuario_por_titulo(self, titulo: TipoUsuarioEnum) -> int:
        query = select(TipoUsuario).where(
            TipoUsuario.titulo == titulo,
            TipoUsuario.deleted_at == None,  # noqa: E711
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_todos_orientandos_de_um_professor(
        self, orientador_id: int
    ) -> Aluno:
        query = (
            select(Aluno)
            .join(Professor, Aluno.orientador_id == Professor.id)
            .join(
                Usuario,
                or_(Usuario.id == Aluno.usuario_id, Usuario.id == Professor.usuario_id),
            )
            .where(
                and_(
                    Professor.id == orientador_id,
                    Aluno.deleted_at == None,  # noqa: E711
                    Professor.deleted_at == None,  # noqa: E711
                    Usuario.deleted_at == None,  # noqa: E711
                )
            )
        )
        result = await self._session.execute(query)
        return result.scalars().unique().all()

    async def buscar_aluno_por_cpf(self, cpf: str) -> Optional[Aluno]:
        query = select(Aluno).where(
            and_(
                Aluno.cpf == cpf,
                Aluno.deleted_at == None,  # noqa: E711
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_lista_de_solicitacoes_de_professor(
        self, professor_id: int, status: StatusSolicitacaoEnum
    ) -> list[Solicitacao]:
        query = (
            select(Solicitacao)
            .join(Professor, Solicitacao.professor_id == Professor.id)
            .join(Usuario, Usuario.id == Professor.usuario_id)
            .where(
                and_(
                    Professor.id == professor_id,
                    Solicitacao.status == status,
                    Solicitacao.deleted_at == None,  # noqa: E711
                    Professor.deleted_at == None,  # noqa: E711
                    Usuario.deleted_at == None,  # noqa: E711
                )
            )
        )
        result = await self._session.execute(query)
        return result.scalars().unique().all()

    async def buscar_usuario_por_email_excluindo_id(
        self, email: str, usuario_id: int
    ) -> Optional[Usuario]:
        query = select(Usuario).where(
            and_(
                Usuario.email == email,
                Usuario.id != usuario_id,
                Usuario.deleted_at == None,  # noqa: E711
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_aluno_por_telefone(self, telefone: str) -> Optional[Aluno]:
        query = select(Aluno).where(
            and_(
                Aluno.telefone == telefone,
                Aluno.deleted_at == None,  # noqa: E711
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_aluno_por_telefone_excluindo_id(
        self, telefone: str, id: int
    ) -> Optional[Aluno]:
        query = select(Aluno).where(
            and_(
                Aluno.telefone == telefone,
                Aluno.id != id,
                Aluno.deleted_at == None,  # noqa: E711
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_aluno_por_matricula(self, matricula: str) -> Optional[Aluno]:
        query = select(Aluno).where(
            and_(
                Aluno.matricula == matricula,
                Aluno.deleted_at == None,  # noqa: E711
            )
        )
        result = await self._session.execute(query)
        return result.scalar()

    async def buscar_tarefas_por_aluno_id(self, aluno_id: int) -> list[Tarefa]:
        return await self.filtrar(Tarefa, aluno_id=aluno_id, deleted_at=None)
