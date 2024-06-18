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
    nome: constr(min_length=3, max_length=100)
    email: EmailStr
    tipo_usuario: TipoUsuarioEnum
    senha: constr(min_length=8)


class ProfessorInDB(UsuarioInDB):
    user_id: int
