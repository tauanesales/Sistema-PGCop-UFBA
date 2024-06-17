from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, constr, field_validator
from pydantic_br import CPF
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.api.exceptions.value_error_validation_exception import MatriculaNotNumericError
from src.api.schemas.usuario import UsuarioBase, UsuarioCreate, UsuarioInDB
from src.api.utils.enums import CursoAlunoEnum, TipoUsuarioEnum

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
    def validar_string_vazia(cls, value):
        value = value.replace("\t", "").replace("\r", "").replace("\n", "")
        if not value.replace(" ", ""):
            raise ValueError("O campo não pode estar em branco")
        return value

    @field_validator("matricula", mode="after")
    def validar_matricula(cls, matricula: str):
        if not matricula.isnumeric():
            raise MatriculaNotNumericError()
        return matricula

    @field_validator("telefone", mode="before")
    def validate_telefone(cls, value):
        return (
            value.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
        )

    @field_validator("lattes")
    def validar_lattes(cls, lattes: str):
        HttpUrl(lattes)
        return lattes


class AlunoCreate(AlunoBase, UsuarioCreate):
    pass


class AlunoInDB(AlunoBase, UsuarioInDB):
    pass


class AlunoUpdate(BaseModel):
    telefone: PhoneNumber = Field(..., description="Número de telefone do aluno.")
    lattes: Optional[constr(min_length=2, max_length=100)] = Field(
        None, description="Link para o currículo Lattes do aluno."
    )
    orientador_id: Optional[int] = Field(
        None, description="ID do orientador do aluno, se houver."
    )
    data_qualificacao: Optional[date] = Field(
        None, description="Data de qualificação do aluno, se aplicável."
    )
    data_defesa: Optional[date] = Field(
        None, description="Data de defesa do aluno, se aplicável."
    )

    @field_validator("telefone", mode="before")
    def blank_string(cls, value):
        return (
            value.replace(" ", "").replace("\t", "").replace("\r", "").replace("\n", "")
        )

    @field_validator("lattes")
    def validar_lattes(cls, lattes: str):
        HttpUrl(lattes)
        return lattes
