from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from src.api.database.models.entity_model_base import EntityModelBase
from src.api.utils.enums import TipoUsuarioEnum


class TipoUsuario(EntityModelBase):
    __tablename__ = "tipo_usuario"

    titulo: Mapped[TipoUsuarioEnum] = mapped_column(
        Enum(TipoUsuarioEnum), nullable=False, index=True
    )
    descricao: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
