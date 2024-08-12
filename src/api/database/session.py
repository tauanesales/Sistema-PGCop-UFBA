from fastapi import HTTPException
from loguru import logger
from pydantic import ValidationError
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool

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
        # query={"charset": "UTF8MB4"},
        query={},
    ),
    poolclass=AsyncAdaptedQueuePool
    if Config.DB_CONFIG.DB_ENABLE_CONNECTION_POOLING
    else NullPool,
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def get_repo(repository=PGCopRepository):
    async def _get_repo():
        async with async_session() as session:
            try:
                yield repository(session)
                await session.commit()
            except Exception as e:
                await session.rollback()
                if not isinstance(e, (HTTPException, ValidationError)):
                    logger.warning(
                        f"Rollback realizado na transação atual devido ao erro: {e};"
                    )
                raise e
            finally:
                await session.close()

    return _get_repo
