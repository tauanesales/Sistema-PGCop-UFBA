from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.api.database.models.aluno import Aluno
from src.api.database.models.entity_model_base import EntityModelBase
from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.tipo_usuario import TipoUsuario
from src.api.database.models.usuario import Usuario
from src.api.utils.enums import StatusSolicitacaoEnum, TipoUsuarioEnum


class PGCopRepository:
    @staticmethod
    def obter_usuario_por_email(db: Session, email: str) -> Usuario:
        return (
            db.query(Usuario)
            .filter(
                and_(
                    Usuario.email == email,
                    Usuario.deleted_at == None,  # noqa: E711
                )
            )
            .first()
        )

    @staticmethod
    def obter_aluno_por_email(db: Session, email: str) -> Aluno:
        return (
            db.query(Aluno)
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

    @staticmethod
    def obter_professor_por_email(db: Session, email: str) -> Usuario:
        return (
            db.query(Professor)
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

    @staticmethod
    def obter_usuario_por_id(db: Session, id: int) -> Usuario:
        return (
            db.query(Usuario)
            .filter(and_(Usuario.id == id, Usuario.deleted_at == None))  # noqa: E711
            .first()
        )

    @staticmethod
    def obter_id_tipo_usuario_por_titulo(db: Session, titulo: TipoUsuarioEnum) -> int:
        return (
            db.query(TipoUsuario)
            .filter(
                and_(
                    TipoUsuario.titulo == titulo,
                    TipoUsuario.deleted_at == None,  # noqa: E711
                )
            )
            .first()
            .id
        )

    @staticmethod
    def obter_por_id(db: Session, id: int, model: EntityModelBase) -> EntityModelBase:
        return (
            db.query(model)
            .filter(and_(model.id == id, model.deleted_at == None))  # noqa: E711
            .first()
        )

    @staticmethod
    def obter_todos(db: Session, model: EntityModelBase) -> EntityModelBase:
        return db.query(model).filter(model.deleted_at == None).all()  # noqa: E711

    @staticmethod
    def obter_todos_orientandos_de_um_professor(
        db: Session, orientador_id: int
    ) -> Aluno:
        return (
            db.query(Aluno)
            .filter(
                and_(
                    Aluno.orientador_id == orientador_id,
                    Aluno.deleted_at == None,  # noqa: E711
                )
            )
            .all()
        )

    def obter_aluno_por_cpf(db: Session, cpf: str) -> Aluno:
        return (
            db.query(Aluno)
            .filter(and_(Aluno.cpf == cpf, Aluno.deleted_at == None))  # noqa: E711
            .first()
        )

    def obter_lista_de_solicitacoes_de_professor(
        db: Session, professor_id: int, status: StatusSolicitacaoEnum
    ) -> list[Solicitacao]:
        return (
            db.query(Solicitacao)
            .filter(
                and_(
                    Solicitacao.professor_id == professor_id,
                    Solicitacao.deleted_at == None,  # noqa: E711 # noqa: E711
                    Solicitacao.status == status,
                )
            )
            .all()
        )

    async def obter_usuario_por_email_excluindo_id(
        db: Session, email: str, id: int
    ) -> Usuario:
        return (
            db.query(Usuario)
            .filter(
                and_(
                    Usuario.email == email,
                    Usuario.id != id,
                    Usuario.deleted_at == None,  # noqa: E711
                )
            )
            .first()
        )
