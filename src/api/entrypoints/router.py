from fastapi.routing import APIRouter

from src.api.entrypoints import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
