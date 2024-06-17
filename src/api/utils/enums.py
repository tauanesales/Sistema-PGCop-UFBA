from strenum import StrEnum


class TipoUsuarioEnum(StrEnum):
    COORDENADOR = "coordenador"
    PROFESSOR = "professor"
    ALUNO = "aluno"


class StatusSolicitacaoEnum(StrEnum):
    PENDENTE = "pendente"
    ACEITA = "aceita"
    RECUSADA = "recusada"


class CursoAlunoEnum(StrEnum):
    MESTRADO = "M"
    DOUTORADO = "D"
