from datetime import date
from typing import Optional

from pydantic import Field, constr, field_validator
from pydantic_br import CPF
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.api.entrypoints.professores.schema import ProfessorInDB
from src.api.exceptions.value_error_validation_exception import MatriculaNotNumericError, InvalidLattesError
from src.api.schemas.usuario import UsuarioBase, UsuarioInDB, UsuarioNovo
from src.api.utils.decorators import partial_model
from src.api.utils.enums import CursoAlunoEnum, TipoUsuarioEnum

import httpx
import re

PhoneNumber.phone_format = "NATIONAL"
PhoneNumber.default_region_code = "BR"
PhoneNumber.min_length = 10
PhoneNumber.max_length = 22


class AlunoBase(UsuarioBase):
    cpf: CPF = Field(..., description="CPF do aluno.")
    telefone: PhoneNumber = Field(..., description="Número de telefone do aluno.")
    matricula: constr(min_length=6, max_length=12) = Field(
        ..., description="Matrícula do aluno."
    )
    orientador_id: Optional[int] = Field(
        None, description="ID do orientador do aluno, se houver."
    )
    curso: CursoAlunoEnum = Field(
        ..., description="Curso do aluno, Mestrado (M) ou Doutorado (D)."
    )
    lattes: Optional[constr(min_length=2, max_length=100)] = Field(
        None, description="Link para o currículo Lattes do aluno."
    )
    data_ingresso: date = Field(..., description="Data de ingresso do aluno no curso.")
    data_qualificacao: Optional[date] = Field(
        None, description="Data de qualificação do aluno, se aplicável."
    )
    data_defesa: Optional[date] = Field(
        None, description="Data de defesa do aluno, se aplicável."
    )
    tipo_usuario: TipoUsuarioEnum = TipoUsuarioEnum.ALUNO

    @field_validator("telefone", "matricula", "lattes", mode="before")
    def validar_string_vazia(cls, valor):
        valor = valor.replace("\t", "").replace("\r", "").replace("\n", "")
        if not valor.replace(" ", ""):
            raise ValueError("O campo não pode estar em branco")
        return valor

    @field_validator("matricula", mode="after")
    def validar_matricula(cls, matricula: str):
        if not matricula.isnumeric():
            raise MatriculaNotNumericError()
        return matricula

    @field_validator("telefone", mode="before")
    def validar_telefone(cls, valor):
        return (
            valor.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
        )

    @field_validator("cpf", mode="after")
    def validar_cpf(cls, valor):
        return valor.replace(".", "").replace("-", "")


class AlunoNovo(AlunoBase, UsuarioNovo):
    @field_validator("lattes", mode='after')
    async def validar_lattes(cls, lattes: str):
        match = re.match(r"http(s?):\/\/lattes\.cnpq\.br\/(.+)", lattes)

        if match is None:
            raise InvalidLattesError()

        lattes_id = match.groups()[1]

        async with httpx.AsyncClient() as client:
            resp = await client.head(
                f"http://buscatextual.cnpq.br/buscatextual/cv?id={lattes_id}",
                headers={"User-Agent": "Chrome/126.0.0.0"}
            )

        if (resp.headers.get("Location") == "http://buscatextual.cnpq.br/buscatextual/erro.jsp"):
            raise InvalidLattesError()
        
        return lattes


class AlunoInDB(AlunoBase, UsuarioInDB):
    usuario_id: int
    orientador: Optional[ProfessorInDB] = Field(
        None, description="Dados do orientador do aluno, se houver."
    )


@partial_model
class AlunoAtualizado(AlunoNovo):
    pass
