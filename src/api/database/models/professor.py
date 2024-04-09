from sqlalchemy import Column, Integer
from src.api.database.session import Base


class Professor(Base):
    __tablename__ = "PROFESSORES"
    ProfessorID = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, nullable=False)
