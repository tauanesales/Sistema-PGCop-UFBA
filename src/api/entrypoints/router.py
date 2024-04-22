from fastapi.routing import APIRouter

from src.api.entrypoints import alunos
from src.api.entrypoints import mailer
from src.api.entrypoints import monitoring
from src.api.entrypoints import usuarios
from src.api.entrypoints import token
from src.api.entrypoints import tarefas

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(alunos.router, prefix="/alunos", tags=["Alunos"])
api_router.include_router(token.router, prefix="/token", tags=["Token"])
api_router.include_router(tarefas.router, prefix="/tarefas", tags=["Tarefas"])
api_router.include_router(mailer.router, prefix="/mailer", tags=["Mailer"])

