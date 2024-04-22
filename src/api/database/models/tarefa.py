
from sqlalchemy import Column, Date, Integer, String
from src.api.database.session import Base

class Tarefa(Base):
    __tablename__ = "TAREFAS"
    ID = Column(Integer, primary_key=True, index=False)
    Descricao = Column(String, nullable=False)
    Data_Prazo = Column(Date, nullable=True)
    Completada = Column(Integer,nullable=True)
    Aluno_ID = Column(Integer, nullable=False)
    Data_Conclusao = Column(Date, nullable=True)
    Last_Notifield = Column(Date, nullable=True)
    
