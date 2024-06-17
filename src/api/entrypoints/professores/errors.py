from fastapi import HTTPException


class EmailAlreadyRegisteredException(HTTPException):
    """
    Use this exception when trying to create
    a new user with an existing email.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Email já cadastrado")


class ProfessorNotFoundException(HTTPException):
    """
    Use this exception when it is not possible
    to find the user which the request requires.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Professor não encontrado")
