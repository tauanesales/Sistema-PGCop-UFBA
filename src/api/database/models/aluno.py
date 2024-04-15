from sqlalchemy import Column, Date, Integer, String
from src.api.database.session import Base


class Aluno(Base):
    __tablename__ = "ALUNOS"
    AlunoID = Column(Integer, primary_key=True, index=True)
    Nome = Column(String, nullable=False, unique=False, index=True)
    Cpf = Column(String, nullable=False, unique=True, index=True)
    Email = Column(String, unique=True, index=True, nullable=False)
    Telefone = Column(String, nullable=False, unique=True, index=True)
    Matricula = Column(String, nullable=False, unique=True, index=True)
    ProfessorID = Column(Integer, nullable=False, index=True)
    Role = Column(Enum("mestrando", "doutorando"), nullable=False)
    DataDeIngresso = Column(Date, nullable=False)
