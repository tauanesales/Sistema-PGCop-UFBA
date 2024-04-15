from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    """
    Use this exception when it is not possible
    to find the user which the request requires.
    """
    def __init__(self):
        super().__init__(status_code=404, detail="Usuário não encontrado")