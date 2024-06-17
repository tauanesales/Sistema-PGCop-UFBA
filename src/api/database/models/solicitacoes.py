from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.entity_model_base import EntityModelBase
from src.api.utils.enums import StatusSolicitacaoEnum


class Solicitacao(EntityModelBase):
    __tablename__ = "solicitacoes"

    aluno_id: Mapped[int] = mapped_column(ForeignKey("alunos.id"), nullable=False)
    aluno: Mapped["Aluno"] = relationship(  # noqa: F821
        "Aluno", back_populates="solicitacoes"
    )

    professor_id: Mapped[int] = mapped_column(
        ForeignKey("professores.id"), nullable=False, unique=False, index=True
    )
    professor: Mapped["Professor"] = relationship(  # noqa: F821
        "Professor", back_populates="solicitacoes"
    )

    status: Mapped[StatusSolicitacaoEnum] = mapped_column(
        Enum(StatusSolicitacaoEnum), nullable=False, index=True
    )
