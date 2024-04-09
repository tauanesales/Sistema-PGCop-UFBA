from sqlalchemy import Column, Date, Integer, String
from src.api.database.session import Base


class Aluno(Base):
    __tablename__ = "ALUNOS"
    AlunoID = Column(Integer, primary_key=True, index=True)
    Matricula = Column(String, nullable=False, unique=True, index=True)
    DataDeIngresso = Column(Date, nullable=False)
    ProfessorID = Column(Integer, nullable=False, index=True)
