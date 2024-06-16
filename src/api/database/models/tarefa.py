from sqlalchemy import Column, Date, Integer, String
from src.api.database.session import Base

class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    completada = Column(Integer,nullable=False, default=0)
    data_prazo = Column(Date, nullable=False)
    aluno_id = Column(Integer, nullable=False)
    last_notified = Column(Date, nullable=True)
    data_conclusao = Column(Date, nullable=True)