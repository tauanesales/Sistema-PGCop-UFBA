from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.entrypoints.professores.schema import (
    ProfessorBase,
    ProfessorCreate,
    ProfessorInDB,
)
from src.api.services.professor import ServiceProfessor

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=ProfessorInDB, status_code=status.HTTP_201_CREATED)
def criar_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    return ServiceProfessor.criar_professor(db=db, professor=professor)


@router.get("/me", response_model=ProfessorInDB)
async def read_professor_me(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return ServiceProfessor.get_current_professor(token, db)


@router.get("/todos", response_model=List[ProfessorInDB])
def obter_todos_professores(db: Session = Depends(get_db)):
    return ServiceProfessor.obter_professores(db)


@router.get("/{professor_id}", response_model=ProfessorInDB)
def ler_professor(professor_id: int, db: Session = Depends(get_db)):
    return ServiceProfessor.obter_professor(db, professor_id=professor_id)


@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_professor(professor_id: int, db: Session = Depends(get_db)):
    ServiceProfessor.deletar_professor(db, professor_id)
    return {"ok": True}


@router.put("/{professor_id}", response_model=ProfessorInDB)
def atualizar_professor(
    professor_id: int, professor: ProfessorBase, db: Session = Depends(get_db)
):
    return ServiceProfessor.atualizar_professor(db, professor_id, professor)


@router.get("/email/{email}", response_model=ProfessorInDB)
def obter_professor_por_email(email: str, db: Session = Depends(get_db)):
    return ProfessorInDB(**ServiceProfessor.obter_por_email(db, email=email).__dict__)
