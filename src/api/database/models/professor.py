from sqlalchemy import Column, Enum, Integer, String
from src.api.database.session import Base


class Professor(Base):
    __tablename__ = "professores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=False)
    email = Column(String, nullable=False, unique=True, index=True)
    role = Column(Enum("professor", "orientador", "coordenador"), nullable=False)
    senha_hash = Column(String, nullable=False)