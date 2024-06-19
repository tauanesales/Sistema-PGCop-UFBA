from typing import AsyncGenerator
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.api.config import Config
from src.api.database.repository import PGCopRepository

engine = create_async_engine(
    URL(
        drivername=Config.DB_CONFIG.DB_DRIVERNAME,
        username=Config.DB_CONFIG.DB_USERNAME,
        password=Config.DB_CONFIG.DB_PASSWORD,
        host=Config.DB_CONFIG.DB_HOST,
        port=Config.DB_CONFIG.DB_PORT,
        database=Config.DB_CONFIG.DB_DATABASE,
        query={"charset": "utf8"},
    )
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

def get_repo(repository = PGCopRepository):
    async def _get_repo():
        async with async_session() as session:
            yield repository(session)
    return _get_repo