from pydantic import BaseModel

from src.api.utils.enums import StatusSolicitacaoEnum


class SolicitacaoBase(BaseModel):
    aluno_id: int
    professor_id: int
    status: StatusSolicitacaoEnum


class SolicitacaoCreate(SolicitacaoBase):
    pass


class SolicitacaoInDB(SolicitacaoBase):
    id: int
    nome_aluno: str
    nome_professor: str

    class ConfigDict:
        from_attributes = (
            True  # Utiliza o ORM mode para compatibilidade com o SQLAlchemy
        )
