from fastapi import HTTPException


class UsuarioNaoEncontradoException(HTTPException):
    """Exceção lançada quando um usuário não é encontrado."""

    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Usuário não encontrado.")


class EmailJaRegistradoException(HTTPException):
    """Exceção lançada quando um email já está registrado."""

    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Email já registrado.")


class TipoUsuarioInvalidoException(HTTPException):
    """Exceção lançada quando um tipo de usuário é inválido."""

    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Tipo de usuário inválido.")


class DeveSeSubmeterPeloMenosUmCampoParaAtualizarException(HTTPException):
    """Exceção lançada quando não se submete pelo menos um campo para atualização."""

    def __init__(self) -> None:
        super().__init__(
            status_code=400,
            detail="Deve-se submeter pelo menos um campo para atualização.",
        )
