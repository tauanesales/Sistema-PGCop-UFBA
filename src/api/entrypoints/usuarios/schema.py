from typing import Literal, Union

from pydantic import BaseModel, Field

from src.api.entrypoints.alunos.schema import AlunoInDB
from src.api.entrypoints.professores.schema import ProfessorInDB


class UsuarioInDB(BaseModel):
    tipo: Literal["aluno", "professor"] = Field(
        ..., description="Tipo de usuário, aluno ou professor."
    )
    dados: Union[AlunoInDB, ProfessorInDB] = Field(
        ..., description="Informações do usuário."
    )
