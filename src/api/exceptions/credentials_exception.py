from fastapi import HTTPException, status


class CredenciaisInvalidasException(HTTPException):
    """
    Exceção para credenciais inválidas.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )


class NaoAutorizadoException(HTTPException):
    """
    Exceção para nível de acesso inválido.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não autorizado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
