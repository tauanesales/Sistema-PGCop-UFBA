from sqlalchemy import Column, Date, Enum, Integer, String
from src.api.database.session import Base


class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=False, index=False)
    cpf = Column(String, nullable=False, unique=True, index=True)
    email_ufba = Column(String, unique=True, index=True, nullable=False)
    matricula = Column(String, nullable=False, unique=True, index=True)
    lattes = Column(String, nullable=True, index=False)
    orientador_id = Column(Integer, nullable=True, index=True)
    curso = Column(Enum("M", "D"), nullable=False)
    data_ingresso = Column(Date, nullable=True)
    data_qualificacao = Column(Date, nullable=False)
    data_defesa = Column(Date, nullable=False)
    senha_hash = Column(String, nullable=False)
