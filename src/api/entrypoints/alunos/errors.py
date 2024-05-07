from fastapi import HTTPException


class CPFAlreadyRegisteredException(HTTPException):
    """
    Use this exception when trying to create 
    a new student with an existing CPF.
    """
    def __init__(self):
        super().__init__(status_code=400, detail="CPF já cadastrado")

class EmailAlreadyRegisteredException(HTTPException):
    """
    Use this exception when trying to create 
    a new student with an existing CPF.
    """
    def __init__(self):
        super().__init__(status_code=400, detail="Email já cadastrado")

class MatriculaAlreadyRegisteredException(HTTPException):
    """
    Use this exception when trying to create 
    a new student with an existing CPF.
    """
    def __init__(self):
        super().__init__(status_code=400, detail="Matrícula já cadastrada")

class StudentNotFoundException(HTTPException):
    """
    Use this exception when it is not possible
    to find the student which the request requires.
    """
    def __init__(self):
        super().__init__(status_code=404, detail="Aluno não encontrado")

class ExcecaoIdOrientadorNaoEncontrado(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Erro ao adicionar aluno: Id do orientador não encontrado. Caso o aluno não tenha orientador, coloque o valor como `null`.")

class ExcecaoGenerica(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Erro ao adicionar aluno: Verifique os dados enviados ou tente novamente mais tarde.")