from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.api.database.session import Base


class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True, index=False)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    completada = Column(Integer, nullable=False, default=0)
    data_prazo = Column(Date, nullable=False)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    aluno = relationship("Aluno", back_populates="tarefas")
    last_notified = Column(Date, nullable=True)
    data_conclusao = Column(Date, nullable=True)
