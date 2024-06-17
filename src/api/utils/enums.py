from enum import auto

from strenum import StrEnum


class TipoUsuarioEnum(StrEnum):
    COORDENADOR = auto()
    PROFESSOR = auto()
    ALUNO = auto()


class StatusSolicitacaoEnum(StrEnum):
    PENDENTE = "pendente"
    ACEITA = "aceita"
    RECUSADA = "recusada"


class CursoAlunoEnum(StrEnum):
    MESTRADO = "M"
    DOUTORADO = "D"
