from typing import Optional
from sqlalchemy import and_, or_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import class_mapper

from src.api.database.models.aluno import Aluno
from src.api.database.models.entity_model_base import EntityModelBase
from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.tipo_usuario import TipoUsuario
from src.api.database.models.usuario import Usuario
from src.api.utils.enums import StatusSolicitacaoEnum, TipoUsuarioEnum


class PGCopRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def buscar_por_id(self, id: int, model: EntityModelBase) -> Optional[EntityModelBase]:
        query = select(model).where(and_(model.id == id, model.deleted_at == None))
        result = await self._session.execute(query)
        return result.scalar()

    async def filtrar(self, model: EntityModelBase, **kwargs) -> list[EntityModelBase]:
        return await self._session.execute(select(model).filter_by(**kwargs)).fetchall()
        
    async def criar(self, model: EntityModelBase) -> EntityModelBase:
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return model
        
    async def atualizar_por_id(self, id: int, model: EntityModelBase, **kwargs) -> EntityModelBase:
        await self._session.execute(
            update(model).where(model.id == id).values(**kwargs)
        )
        return await self.buscar_por_id(id, model)

    async def buscar_usuario_por_email(self, email: str) -> Optional[Usuario]:
        return (
            self._session.query(Usuario)
            .filter(
                and_(
                    Usuario.email == email,
                    Usuario.deleted_at == None,  # noqa: E711
                )
            )
            .first()
        )

    async def buscar_aluno_por_email(self, email: str) -> Optional[Aluno]:
        return (
            self._session.query(Aluno)
            .join(Usuario, Usuario.id == Aluno.usuario_id)
            .filter(
                and_(
                    Usuario.email == email,
                    Usuario.deleted_at == None,  # noqa: E711
                    Aluno.deleted_at == None,  # noqa: E711
                )
            )
            .first()
        )

    async def buscar_professor_por_email(self, email: str) -> Optional[Usuario]:
        return (
            self._session.query(Professor)
            .join(Usuario, Professor.usuario_id == Usuario.id)
            .join(TipoUsuario, Usuario.tipo_usuario_id == TipoUsuario.id)
            .filter(
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
            .first()
        )

    async def buscar_usuario_por_id(self, id: int) -> Optional[Usuario]:
        return await self.buscar_por_id(id, Usuario)

    async def buscar_id_tipo_usuario_por_titulo(self, titulo: TipoUsuarioEnum) -> int:
        return (
            self._session.query(TipoUsuario)
            .filter(
                and_(
                    TipoUsuario.titulo == titulo,
                    TipoUsuario.deleted_at == None,  # noqa: E711
                )
            )
            .first()
            .id
        )


    async def buscar_todos(self, model: EntityModelBase) -> list[EntityModelBase]:
        async with self._session.begin():
            return (await self._session.execute(select(model).where(model.deleted_at == None))).fetchall()  # noqa: E711

    async def buscar_todos_orientandos_de_um_professor(self, 
        orientador_id: int
    ) -> Aluno:
        return (
            self._session.query(Aluno)
            .filter(
                and_(
                    Aluno.orientador_id == orientador_id,
                    Aluno.deleted_at == None,  # noqa: E711
                )
            )
            .all()
        )

    async def buscar_aluno_por_cpf(self, cpf: str) -> Optional[Aluno]:
        return (
            self._session.query(Aluno)
            .filter(and_(Aluno.cpf == cpf, Aluno.deleted_at == None))  # noqa: E711
            .first()
        )

    def buscar_lista_de_solicitacoes_de_professor(self,
        professor_id: int, status: StatusSolicitacaoEnum
    ) -> list[Solicitacao]:
        return (
            self._session.query(Solicitacao)
            .filter(
                and_(
                    Solicitacao.professor_id == professor_id,
                    Solicitacao.deleted_at == None,  # noqa: E711 # noqa: E711
                    Solicitacao.status == status,
                )
            )
            .all()
        )

    async def buscar_usuario_por_email_excluindo_id(self, 
        email: str, id: int
    ) -> Optional[Usuario]:
        return (
            self._session.query(Usuario)
            .filter(
                and_(
                    Usuario.email == email,
                    Usuario.id != id,
                    Usuario.deleted_at == None,  # noqa: E711
                )
            )
            .first()
        )
    
    
    async def buscar_aluno_por_telefone(self, telefone: str) -> Optional[Aluno]:
        return (
            self._session.query(Aluno)
            .filter(
                and_(
                    Aluno.telefone == telefone,
                    Aluno.deleted_at == None,  # noqa: E711
                )
            )
            .first()
        )


    async def buscar_aluno_por_telefone_excluindo_id(self, telefone: str, id: int) -> Optional[Aluno]:
        return (
            self._session.query(Aluno)
            .filter(
                and_(
                    Aluno.telefone == telefone,
                    Aluno.id != id,
                    Aluno.deleted_at == None,  # noqa: E711
                )
            )
            .first()
        )
