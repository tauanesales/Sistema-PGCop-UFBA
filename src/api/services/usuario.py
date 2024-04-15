from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.api.database.models.usuario import Usuario
from src.api.entrypoints.usuarios.schema import UsuarioCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServiceUsuario:
    @staticmethod
    def criar_usuario(db: Session, usuario: UsuarioCreate):
        db_usuario = Usuario(
            Nome=usuario.Nome,
            Email=usuario.Email,
            Senha=pwd_context.hash(usuario.Senha),
            Role=usuario.Role,
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    @staticmethod
    def obter_usuario(db: Session, usuario_id: int):
        return db.query(Usuario).filter(Usuario.UserID == usuario_id).one_or_none()

    @staticmethod
    def deletar_usuario(db: Session, usuario_id: int):
        db_usuario = db.query(Usuario).filter(Usuario.UserID == usuario_id).one_or_none()
        if db_usuario:
            db.delete(db_usuario)
            db.commit()
            return True
        return False

    @staticmethod
    def atualizar_usuario(db: Session, usuario_id: int, update_data: dict):
        db.query(Usuario).filter(Usuario.UserID == usuario_id).update(update_data)
        db.commit()
        return db.query(Usuario).filter(Usuario.UserID == usuario_id).one_or_none()

    @staticmethod
    def obter_usuario_por_email(db: Session, email: str):
        return db.query(Usuario).filter(Usuario.Email == email).one_or_none()
