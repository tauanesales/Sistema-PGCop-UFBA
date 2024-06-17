from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.base_model import BaseModel


class Professor(BaseModel):
    __tablename__ = "professores"

    alunos: Mapped["Aluno"] = relationship(  # noqa: F821
        "Aluno", back_populates="orientador"
    )

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    usuario: Mapped["Usuario"] = relationship(  # noqa: F821
        "Usuario", back_populates="professor"
    )
