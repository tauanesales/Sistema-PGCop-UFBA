from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.base_model import BaseModel
from src.api.database.models.tipo_usuario import TipoUsuario


class Usuario(BaseModel):
    __tablename__ = "usuarios"

    nome: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    new_password_token: Mapped[str] = mapped_column(String(255), nullable=True)

    tipo_usuario: Mapped["TipoUsuario"] = relationship("TipoUsuario")
    tipo_usuario_id: Mapped[int] = mapped_column(
        nullable=False, unique=False, index=True
    )
