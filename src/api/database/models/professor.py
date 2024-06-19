from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.entity_model_base import EntityModelBase


class Professor(EntityModelBase):
    __tablename__ = "professores"

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"), nullable=False, unique=False, index=True
    )
    usuario: Mapped["Usuario"] = relationship("Usuario", lazy="joined")  # noqa: F821

    alunos: Mapped[list["Aluno"]] = relationship(  # noqa: F821
        "Aluno",
        back_populates="orientador",
        uselist=True,
        lazy="joined",
    )
    solicitacoes: Mapped[list["Solicitacao"]] = relationship(  # noqa: F821
        "Solicitacao",
        back_populates="professor",
        uselist=True,
        lazy="joined",
    )
