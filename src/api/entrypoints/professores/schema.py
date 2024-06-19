from src.api.schemas.usuario import UsuarioBase, UsuarioCriacao, UsuarioInDB
from src.api.utils.decorators import partial_model


class ProfessorBase(UsuarioBase):
    pass


class ProfessorCreate(UsuarioCriacao):
    pass


@partial_model
class ProfessorUpdate(ProfessorCreate):
    pass


class ProfessorInDB(UsuarioInDB):
    user_id: int
