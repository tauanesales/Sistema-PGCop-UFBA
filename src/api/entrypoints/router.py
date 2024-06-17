from fastapi.routing import APIRouter

from src.api.entrypoints.alunos import views as alunos
from src.api.entrypoints.mailer import views as mailer
from src.api.entrypoints.monitoring import views as monitoring
from src.api.entrypoints.new_password import views as new_password
from src.api.entrypoints.professores import views as professores
from src.api.entrypoints.tarefas import views as tarefas
from src.api.entrypoints.tarefas_base import views as tarefas_base
from src.api.entrypoints.token import views as token
from src.api.entrypoints.usuarios import views as usuarios

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(
    professores.router, prefix="/professores", tags=["Professores"]
)
api_router.include_router(alunos.router, prefix="/alunos", tags=["Alunos"])
api_router.include_router(token.router, prefix="/token", tags=["Token"])
api_router.include_router(tarefas.router, prefix="/tarefas", tags=["Tarefas"])
api_router.include_router(
    tarefas_base.router, prefix="/tarefas_base", tags=["Tarefas_base"]
)
api_router.include_router(mailer.router, prefix="/mailer", tags=["Mailer"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(
    new_password.router, prefix="/new_password", tags=["New_Password"]
)
