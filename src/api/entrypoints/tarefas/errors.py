from fastapi import HTTPException


#class CPFAlreadyRegisteredException(HTTPException):
#    """
#    Use this exception when trying to create 
#    a new student with an existing CPF.
#    """
#    def __init__(self):
#        super().__init__(status_code=400, detail="CPF já cadastrado")


#class StudentNotFoundException(HTTPException):
#    """
#    Use this exception when it is not possible
#    to find the student which the request requires.
#    """
#    def __init__(self):
#        super().__init__(status_code=404, detail="Aluno não encontrado")