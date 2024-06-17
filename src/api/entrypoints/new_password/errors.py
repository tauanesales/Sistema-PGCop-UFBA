from fastapi import HTTPException


class EmailNotFoundException(HTTPException):
    """
    Use this exception when it is not possible
    to find the user which the request requires.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Email não encontrado")


class AuthenticationException(HTTPException):
    """
    Use this exception when it is not possible
    to authenticate the user which the request requires.
    """

    def __init__(self):
        super().__init__(status_code=403, detail="Usuário não pôde ser autenticado.")
