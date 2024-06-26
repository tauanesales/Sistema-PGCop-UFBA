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


class CPFJaRegistradoException(HTTPException):
    """
    Exceção lançada quando um CPF já está registrado.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="CPF já cadastrado")


class MatriculaJaRegistradaException(HTTPException):
    """
    Exceção lançada quando uma matrícula já está registrada.
    """

    def __init__(self):
        super().__init__(status_code=400, detail="Matrícula já cadastrada")


class AlunoNaoEncontradoException(HTTPException):
    """
    Exceção lançada quando um aluno não é encontrado.

    Atributos:
    - status_code: O código de status HTTP da exceção (404).
    - detail: Uma mensagem detalhada informando que o aluno não foi encontrado.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="Aluno não encontrado")


class OrientadorNaoEncontradoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar aluno: orientador não encontrado.",
        )


class OrientadorDeveSerInformadoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar aluno: orientador deve ser informado.",
        )


class CadastroSemOrientadorNaoEncontradoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar aluno: orientador padrão não encontrado.",
        )


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


class OrientadorInvalidoInformadoException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar aluno: orientador deve ser válido.",
        )
