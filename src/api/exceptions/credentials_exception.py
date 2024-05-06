from fastapi import HTTPException, status


class CredentialsException(HTTPException):
    """
    Use this exception when trying to create 
    a new student with an existing CPF.
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas", headers={"WWW-Authenticate": "Bearer"})
