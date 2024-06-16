from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from src.api.database.session import Base


class Professor(Base):
    __tablename__ = "professores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    role = Column(Enum("orientador", "coordenador"), nullable=False)
    new_password_token = Column(String(255), nullable=True)
    alunos = relationship("Aluno", back_populates="orientador")
