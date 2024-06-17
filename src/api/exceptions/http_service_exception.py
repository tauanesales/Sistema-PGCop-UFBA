from fastapi import HTTPException


class UsuarioNaoEncontradoException(HTTPException):
    """Exceção lançada quando um usuário não é encontrado."""

    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Usuário não encontrado.")


class EmailJaRegistradoException(HTTPException):
    """Exceção lançada quando um email já está registrado."""

    def __init__(self) -> None:
        super().__init__(status_code=400, detail="Email já registrado.")
