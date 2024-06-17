from fastapi import HTTPException


class ExcecaoTarefaNaoEncontrada(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Tarefa não encontrada")


class ExcecaoIdAlunoNaoEncontrado(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar tarefa: Id do aluno não encontrado.",
        )


class ExcecaoGenerica(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Erro ao adicionar tarefa: Verifique os dados enviados ou tente \
                novamente mais tarde.",
        )
