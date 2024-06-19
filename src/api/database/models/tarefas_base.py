from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.api.database.models.entity_model_base import EntityModelBase
from src.api.utils.enums import CursoAlunoEnum


class TarefaBase(EntityModelBase):
    __tablename__ = "tarefas_base"

    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    prazo_em_meses: Mapped[int] = mapped_column(Integer, nullable=False)
    curso: Mapped[CursoAlunoEnum] = mapped_column(
        Enum(CursoAlunoEnum), nullable=False, index=True
    )
