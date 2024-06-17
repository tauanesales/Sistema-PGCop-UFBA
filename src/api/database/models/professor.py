from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.entity_model_base import EntityModelBase


class Professor(EntityModelBase):
    __tablename__ = "professores"

    alunos: Mapped["Aluno"] = relationship(  # noqa: F821
        "Aluno", back_populates="orientador"
    )
    solicitacoes: Mapped["Solicitacao"] = relationship(  # noqa: F821
        "Solicitacao", back_populates="professor"
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False, unique=False, index=True
    )
    usuario: Mapped["Usuario"] = relationship("Usuario")  # noqa: F821
