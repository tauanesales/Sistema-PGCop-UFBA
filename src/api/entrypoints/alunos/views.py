from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.api.database.session import get_db
from src.api.entrypoints.alunos.schema import AlunoCreate, AlunoInDB
from src.api.services.aluno import ServicoAluno

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=AlunoInDB, status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    return ServicoAluno.criar(db, aluno)


@router.get("/me", response_model=AlunoInDB)
async def read_aluno_me(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    return ServicoAluno.buscar_atual(db=db, token=token)


@router.get("/{aluno_id}", response_model=AlunoInDB)
def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    return ServicoAluno.obter_aluno(db, aluno_id)


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    ServicoAluno.deletar(db, aluno_id)
    return {"ok": True}


@router.put("/{aluno_id}", response_model=AlunoInDB)
def atualizar_aluno(aluno_id: int, aluno: dict, db: Session = Depends(get_db)):
    return ServicoAluno.atualizar_aluno(db, aluno_id, aluno)


@router.get("/cpf/{aluno_cpf}", response_model=AlunoInDB)
def get_aluno_cpf(aluno_cpf: str, db: Session = Depends(get_db)):
    return ServicoAluno.obter_aluno_por_cpf(db, aluno_cpf)


@router.get("/email/{aluno_email}", response_model=AlunoInDB)
def get_aluno_email(aluno_email: str, db: Session = Depends(get_db)):
    return ServicoAluno.de_aluno_para_aluno_in_db(
        ServicoAluno.obter_por_email(db, aluno_email)
    )


@router.get("/orientador/{orientador_id}", response_model=List[AlunoInDB])
def get_alunos_por_orientador(orientador_id: int, db: Session = Depends(get_db)):
    return ServicoAluno.obter_alunos_por_orientador(db, orientador_id)
