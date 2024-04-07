from fastapi.routing import APIRouter

from src.api.entrypoints import monitoring
from src.api.entrypoints import usuario
from src.api.entrypoints import token

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(usuario.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(token.router, prefix="/token", tags=["Token"])
