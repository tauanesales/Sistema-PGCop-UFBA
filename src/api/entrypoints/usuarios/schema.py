from typing import Union

from pydantic import BaseModel, Field

from src.api.entrypoints.alunos.schema import AlunoInDB
from src.api.entrypoints.professores.schema import ProfessorInDB
from src.api.utils.enums import TipoUsuarioEnum


class TipoUsuarioInDB(BaseModel):
    tipo: TipoUsuarioEnum = Field(
        ..., description="Tipo de usuário, aluno ou professor."
    )
    dados: Union[AlunoInDB, ProfessorInDB] = Field(
        ..., description="Informações do usuário."
    )
