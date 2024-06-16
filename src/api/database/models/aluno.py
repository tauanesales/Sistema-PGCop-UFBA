from sqlalchemy import Column, Date, Integer, String, Enum
from src.api.database.session import Base


class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, nullable=False, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, unique=False, index=True)
    cpf = Column(String(14), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    telefone = Column(String(20), nullable=False, unique=True, index=True)
    matricula = Column(String(20), nullable=False, unique=True, index=True)
    lattes = Column(String(255), nullable=True, index=True)
    orientador_id = Column(Integer, nullable=True, index=True)
    curso = Column(Enum("M", "D"), nullable=False, index=True)
    data_ingresso = Column(Date, nullable=False, index=True)
    data_qualificacao = Column(Date, nullable=True, index=True)
    data_defesa = Column(Date, nullable=True, index=True)
    senha_hash = Column(String(255), nullable=False, index=True)
    new_password_token = Column(String(255), nullable=True)