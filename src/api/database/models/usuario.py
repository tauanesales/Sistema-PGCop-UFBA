from sqlalchemy import Column, Integer, String, Enum
from src.api.database.session import Base


class Usuario(Base):
    __tablename__ = "USUARIOS"
    UserID = Column(Integer, primary_key=True, index=True)
    Nome = Column(String)
    Email = Column(String, unique=True, index=True, nullable=False)
    Senha = Column(String, nullable=False)
    Role = Column(Enum("professor", "orientador", "coordenador"), nullable=False)
