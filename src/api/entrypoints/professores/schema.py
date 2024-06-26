from pydantic import BaseModel

from src.api.schemas.usuario import UsuarioBase, UsuarioInDB, UsuarioNovo
from src.api.utils.decorators import partial_model


class ProfessorBase(UsuarioBase):
    pass


class ProfessorNovo(ProfessorBase, UsuarioNovo):
    pass


class ProfessorInDB(UsuarioInDB):
    pass


@partial_model
class ProfessorAtualizado(ProfessorNovo):
    pass


class ProfessorResponse(BaseModel):
    id: int
    nome: str
