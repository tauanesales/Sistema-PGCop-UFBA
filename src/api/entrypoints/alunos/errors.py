from fastapi import HTTPException


class CPFAlreadyRegisteredException(HTTPException):
    """
    Use this exception when trying to create
    a new student with an existing CPF.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="CPF já cadastrado")


class EmailJaRegistradoException(HTTPException):
    """
    Use this exception when trying to create
    a new student with an existing CPF.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Email já cadastrado")


class MatriculaJaRegistradaException(HTTPException):
    """
    Use this exception when trying to create
    a new student with an existing CPF.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Matrícula já cadastrada")


class AlunoNaoEncontradoException(HTTPException):
    """
    Use this exception when it is not possible
    to find the student which the request requires.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Aluno não encontrado")


class OrientadorNaoEncontradoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar aluno: Id do orientador não encontrado.",
        )
        # Caso o aluno não tenha orientador, coloque o valor como `null`.")
        # TODO: Aluno pode ser cadastrado sem orientador?
        #   Se sim, coluna de orientador_id deve ser nullable no banco de dados/schema.
        #       Nesse caso, alterar o schema, `make revision` -> `make migrate`
        #   Se não, apenas apagar esses comentários.


class ExcecaoGenerica(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar aluno: \
                Verifique os dados enviados ou tente novamente mais tarde.",
        )


class NumeroJaRegistradoException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Telefone já cadastrado")
