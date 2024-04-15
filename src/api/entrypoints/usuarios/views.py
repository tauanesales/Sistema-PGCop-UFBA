from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from src.api.database.session import get_db
from src.api.entrypoints.usuarios.errors import EmailAlreadyRegisteredException, UserNotFoundException
from src.api.entrypoints.usuarios.schema import UsuarioBase, UsuarioCreate, UsuarioInDB
from src.api.services.usuario import ServiceUsuario


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=UsuarioInDB, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return ServiceUsuario.criar_usuario(db=db, usuario=usuario)


@router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.get("/{usuario_id}", response_model=UsuarioInDB)
def ler_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return ServiceUsuario.obter_usuario(db, usuario_id=usuario_id)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    ServiceUsuario.deletar_usuario(db, usuario_id)
    return {"ok": True}


@router.put("/{usuario_id}", response_model=UsuarioInDB)
def atualizar_usuario(usuario_id: int, usuario: UsuarioBase, db: Session = Depends(get_db)):
    return ServiceUsuario.atualizar_usuario(db, usuario_id, usuario.dict())


@router.get("/email/{email}", response_model=UsuarioInDB)
def obter_usuario_por_email(email: str, db: Session = Depends(get_db)):
    return ServiceUsuario.obter_usuario_por_email(db, email=email)
