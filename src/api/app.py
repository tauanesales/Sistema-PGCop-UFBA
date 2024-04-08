from pathlib import Path

from src.api.entrypoints.router import api_router
from src.api.mailsender import mailer

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

import asyncio


APP_ROOT = Path(__file__).parent


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    _app = FastAPI(
        title="fastapi-backend",
        default_response_class=JSONResponse,
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.include_router(router=api_router)

    @_app.on_event("startup")
    async def app_startup():
        asyncio.create_task(mailer.start_mailer())

    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    return _app
