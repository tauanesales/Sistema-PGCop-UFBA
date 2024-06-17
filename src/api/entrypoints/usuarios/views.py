from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.entrypoints.usuarios.schema import TipoUsuarioInDB
from src.api.services.tipo_usuario import TipoUsuarioService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=TipoUsuarioInDB)
async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return TipoUsuarioService.obter_usuario_atual(db=db, token=token)
