from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.entity_model_base import EntityModelBase


class Usuario(EntityModelBase):
    __tablename__ = "usuarios"

    nome: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    token_nova_senha: Mapped[str] = mapped_column(String(255), nullable=True)

    tipo_usuario: Mapped["TipoUsuario"] = relationship(  # noqa: F821
        "TipoUsuario", lazy="joined"
    )
    tipo_usuario_id: Mapped[int] = mapped_column(
        ForeignKey("tipo_usuario.id"), nullable=False, unique=False, index=True
    )
