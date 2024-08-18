from datetime import date
from typing import Optional

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.database.models.entity_model_base import EntityModelBase
from src.api.utils.enums import CursoAlunoEnum


class Aluno(EntityModelBase):
    __tablename__ = "alunos"

    cpf: Mapped[str] = mapped_column(
        String(14), nullable=False, unique=False, index=True
    )
    telefone: Mapped[str] = mapped_column(
        String(23), nullable=False, unique=False, index=True
    )
    matricula: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=False, index=True
    )
    lattes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    curso: Mapped[CursoAlunoEnum] = mapped_column(nullable=False, index=True)
    data_ingresso: Mapped[date] = mapped_column(Date(), nullable=False, index=True)
    data_qualificacao: Mapped[Optional[date]] = mapped_column(Date(), nullable=True, index=True)
    data_defesa: Mapped[Optional[date]] = mapped_column(Date(), nullable=True, index=True)

    orientador_id: Mapped[int] = mapped_column(
        ForeignKey("professores.id"), nullable=True, index=True
    )

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    usuario: Mapped["Usuario"] = relationship(  # noqa: F821
        "Usuario",
        lazy="joined",
    )

    tarefas: Mapped[list["Tarefa"]] = relationship(  # noqa: F821
        "Tarefa",
        back_populates="aluno",
        uselist=True,
        lazy="joined",
    )
    orientador: Mapped["Professor"] = relationship(  # noqa: F821
        "Professor",
        back_populates="alunos",
        lazy="joined",
    )
    solicitacoes: Mapped[list["Solicitacao"]] = relationship(  # noqa: F821
        "Solicitacao",
        back_populates="aluno",
        lazy="joined",
    )
