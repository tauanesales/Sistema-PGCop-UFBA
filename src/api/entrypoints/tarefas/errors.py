from fastapi import HTTPException

class ExcecaoTarefaNaoEncontrada(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Tarefa não encontrada")