from sqlalchemy import Column, Date, Enum, Integer, String
from src.api.database.session import Base


class Tarefa(Base):
    __tablename__ = "TAREFASTESTE"
    TarefaID = Column(Integer, primary_key=True, index=False)
    Descricao = Column(String, nullable=False)
    Prazo = Column(Date, nullable=True)
    #Status = Column(Enum("pendente", "completa", "atrasada"), nullable=False)
    #AlunoID = Column(Integer, nullable=True, index=True)
    ProfessorID = Column(Integer, nullable=False, index=True)
