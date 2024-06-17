from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.entrypoints.alunos.errors import StudentNotFoundException
from src.api.entrypoints.professores.errors import ProfessorNotFoundException
from src.api.entrypoints.usuarios.schema import UsuarioInDB
from src.api.services.aluno import ServiceAluno
from src.api.services.professor import ServiceProfessor

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/me", response_model=UsuarioInDB)
async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    try:
        return UsuarioInDB(
            tipo="aluno", dados=ServiceAluno.get_current_aluno(token, db)
        )
    except StudentNotFoundException:
        pass

    try:
        return UsuarioInDB(
            tipo="professor", dados=ServiceProfessor.get_current_professor(token, db)
        )
    except ProfessorNotFoundException:
        pass

    raise HTTPException(status_code=404, detail="Usuário não encontrado")
