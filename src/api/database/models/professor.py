from sqlalchemy import Column, Integer, String, Enum
from src.api.database.session import Base

class Professor(Base):
    tablename = "professores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String,nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)
    role = Column(Enum("professor", "orientador", "coordenador"), nullable=False)
