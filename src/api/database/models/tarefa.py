
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from src.api.database.session import Base

class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    completada = Column(Integer, nullable=True)
    data_prazo = Column(Date, nullable=False)
    aluno_id = Column(ForeignKey("aluno.id"), nullable=True, index=True)
    
