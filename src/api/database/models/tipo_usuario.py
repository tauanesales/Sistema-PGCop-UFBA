from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.api.database.models.base_model import BaseModel
from src.api.utils.enums import TipoUsuarioEnum


class TipoUsuario(BaseModel):
    __tablename__ = "tipo_usuario"

    tipo_usuario: Mapped[TipoUsuarioEnum] = mapped_column(
        Enum(TipoUsuarioEnum), nullable=False, index=True
    )
