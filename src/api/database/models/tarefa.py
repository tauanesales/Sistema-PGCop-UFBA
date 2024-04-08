from sqlalchemy import Column, Date, Enum, Integer, String
from src.api.database.session import Base


class Tarefa(Base):
    __tablename__ = "TAREFAS"
    TarefaID = Column(Integer, primary_key=True, index=True)
    Descricao = Column(String, nullable=False)
    Prazo = Column(Date, nullable=False)
    Status = Column(Enum("pendente", "completa", "atrasada"), nullable=False)
    AlunoID = Column(Integer, nullable=False, index=True)
    ProfessorID = Column(Integer, nullable=False, index=True)
