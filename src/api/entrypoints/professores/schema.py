from src.api.schemas.usuario import UsuarioBase, UsuarioCreate, UsuarioInDB


class ProfessorBase(UsuarioBase):
    pass


class ProfessorCreate(UsuarioCreate):
    pass


class ProfessorInDB(UsuarioInDB):
    user_id: int
