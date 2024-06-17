from sqlalchemy import Column, Enum, Integer, String, Text

from src.api.database.session import Base


class TarefasBase(Base):
    __tablename__ = "tarefas_base"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False)
    prazo_em_meses = Column(Integer, nullable=False)
    curso = Column(Enum("M", "D"), nullable=False, index=True)
