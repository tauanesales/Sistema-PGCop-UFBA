from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.entity_model_base import EntityModelBase


class Tarefa(EntityModelBase):
    __tablename__ = "tarefas"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    data_ultima_notificacao: Mapped[datetime] = mapped_column(
        DateTime(), nullable=False, default=datetime.utcnow()
    )
    data_prazo: Mapped[date] = mapped_column(Date(), nullable=False)
    data_conclusao: Mapped[Optional[date]] = mapped_column(Date(), nullable=True)

    aluno_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("alunos.id"), nullable=False, unique=False, index=True
    )
    aluno: Mapped["Aluno"] = relationship(  # noqa: F821
        "Aluno",
        back_populates="tarefas",
        lazy="joined",
    )
