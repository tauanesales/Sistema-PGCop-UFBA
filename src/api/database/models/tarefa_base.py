
from sqlalchemy import Column, Enum, Integer, String
from src.api.database.session import Base

class TarefaBase(Base):
    __tablename__ = "tarefas_base"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    prazo_em_meses = Column(Integer, nullable=False)
    curso = Column(Enum("M", "D"), nullable=False)
    
