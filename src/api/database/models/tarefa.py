from sqlalchemy import Column, Date, Enum, Integer, String
from src.api.database.session import Base


class Tarefa(Base):
    __tablename__ = "TAREFAS"
    TarefaID = Column(Integer, primary_key=True, index=True)
    Descricao = Column(String, nullable=False)
    Prazo = Column(Date, nullable=True)
    Status = Column(Enum("pendente", "completa", "atrasada"), nullable=True)
    AlunoID = Column(Integer, nullable=True, index=True)
    ProfessorID = Column(Integer, nullable=True, index=True)
