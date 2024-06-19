from pydantic import EmailStr, constr

from src.api.schemas.usuario import UsuarioBase, UsuarioCreate, UsuarioInDB
from src.api.utils.decorators import partial_model
from src.api.utils.enums import TipoUsuarioEnum


class ProfessorBase(UsuarioBase):
    pass


class ProfessorCreate(UsuarioCreate):
    pass


@partial_model
class ProfessorUpdate(ProfessorCreate):
    pass


class ProfessorInDB(UsuarioInDB):
    user_id: int
