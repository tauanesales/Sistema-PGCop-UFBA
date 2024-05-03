from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


from src.api.database.session import get_db
from src.api.entrypoints.professores.errors import EmailAlreadyRegisteredException, UserNotFoundException
from src.api.entrypoints.professores.schema import ProfessorBase, ProfessorCreate, ProfessorInDB
from src.api.services.professor import ServiceProfessor


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=ProfessorInDB, status_code=status.HTTP_201_CREATED)
def criar_professor(usuario: ProfessorCreate, db: Session = Depends(get_db)):
    return ServiceProfessor.criar_professor(db=db, professor=usuario)


@router.get("/me")
async def read_professor_me(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.get("/{professor_id}", response_model=ProfessorInDB)
def ler_usuario(professor_id: int, db: Session = Depends(get_db)):
    return ServiceProfessor.obter_professor(db, professor_id=professor_id)


@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_professor(professor_id: int, db: Session = Depends(get_db)):
    ServiceProfessor.deletar_professor(db, professor_id)
    return {"ok": True}


@router.put("/{professor_id}", response_model=ProfessorInDB)
def atualizar_professor(professor_id: int, professor: ProfessorBase, db: Session = Depends(get_db)):
    return ServiceProfessor.atualizar_professor(db, professor_id, professor.dict())


@router.get("/email/{email}", response_model=ProfessorInDB)
def obter_professor_por_email(email: str, db: Session = Depends(get_db)):
    return ServiceProfessor.obter_professor_por_email(db, email=email)
