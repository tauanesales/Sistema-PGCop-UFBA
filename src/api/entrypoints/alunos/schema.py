from datetime import date
from typing import Optional

from pydantic import Field, HttpUrl, constr, field_validator
from pydantic_br import CPF
from pydantic_extra_types.phone_numbers import PhoneNumber

from src.api.entrypoints.professores.schema import ProfessorInDB
from src.api.exceptions.value_error_validation_exception import MatriculaNotNumericError
from src.api.schemas.usuario import UsuarioBase, UsuarioInDB, UsuarioNovo
from src.api.utils.decorators import partial_model
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

    @field_validator("lattes")
    def validar_lattes(cls, lattes: str):
        HttpUrl(lattes)
        return lattes


class AlunoNovo(AlunoBase, UsuarioNovo):
    pass


class AlunoInDB(AlunoBase, UsuarioInDB):
    usuario_id: int

class AlunoInDBProfDict(AlunoInDB):
    orientador_id: Optional[ProfessorInDB] = None

    def __init__(self, id: int, usuario_id: int, nome: str, email: str, tipo_usuario: str, cpf: str,
                 telefone: str, matricula: str, lattes: str, curso: str, data_ingresso: date,
                 data_qualificacao: Optional[date] = None, data_defesa: Optional[date] = None,
                 orientador_id: Optional[ProfessorInDB] = None):
        super().__init__(
            id=id, usuario_id=usuario_id, nome=nome, email=email, tipo_usuario=tipo_usuario,
            cpf=cpf, telefone=telefone, matricula=matricula, lattes=lattes, curso=curso,
            data_ingresso=data_ingresso, data_qualificacao=data_qualificacao, data_defesa=data_defesa,
            orientador_id=orientador_id
        )

@partial_model
class AlunoAtualizado(AlunoNovo):
    pass
