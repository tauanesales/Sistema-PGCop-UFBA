from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.entrypoints.alunos.schema import AlunoCreate, AlunoInDB
from src.api.services.aluno import ServiceAluno

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=AlunoInDB, status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    return ServiceAluno.criar_aluno(db, aluno)


@router.get("/me", response_model=AlunoInDB)
async def read_aluno_me(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return ServiceAluno.get_current_aluno(token, db)


@router.get("/{aluno_id}", response_model=AlunoInDB)
def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    return ServiceAluno.obter_aluno(db, aluno_id)


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    ServiceAluno.deletar_aluno(db, aluno_id)
    return {"ok": True}


@router.put("/{aluno_id}", response_model=AlunoInDB)
def atualizar_aluno(aluno_id: int, aluno: dict, db: Session = Depends(get_db)):
    return ServiceAluno.atualizar_aluno(db, aluno_id, aluno)


@router.get("/cpf/{aluno_cpf}", response_model=AlunoInDB)
def get_aluno_cpf(aluno_cpf: str, db: Session = Depends(get_db)):
    return ServiceAluno.obter_aluno_por_cpf(db, aluno_cpf)


@router.get("/email/{aluno_email}", response_model=AlunoInDB)
def get_aluno_email(aluno_email: str, db: Session = Depends(get_db)):
    return AlunoInDB(**ServiceAluno.obter_por_email(db, aluno_email).__dict__)


@router.get("/orientador/{orientador_id}", response_model=List[AlunoInDB])
def get_alunos_por_orientador(orientador_id: int, db: Session = Depends(get_db)):
    return ServiceAluno.obter_alunos_por_orientador(db, orientador_id)
