# app/core/deps.py
from __future__ import annotations

from functools import lru_cache
from typing import AsyncGenerator, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.redis_client import RedisClient
from app.api.api_client import APIClient
from app.api.jobs_api import JobsAPI
from app.services.jobs_service import JobsService
from app.services.firecrawl import FirecrawlService

# --- SQLAlchemy (Async) -------------------------------------------------------

engine = create_async_engine(
    str(settings.DATABASE_URL),
    pool_size=getattr(settings, "DB_MAX_SIZE", 5),
    max_overflow=0,
    echo=getattr(settings, "DB_ECHO", False),
    future=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError:
            raise


# --- Redis -------------------------------------------------------------------

@lru_cache
def get_redis() -> RedisClient:
    """
    Return a singleton RedisClient wrapper.
    """
    return RedisClient()

# --- JobsService -------------------------------------------------------------

@lru_cache
def get_api_client() -> APIClient:
    return APIClient()

@lru_cache
def get_jobs_api() -> JobsAPI:
    return JobsAPI()

def get_firecrawl_service() -> FirecrawlService:
    return FirecrawlService(get_redis())

def get_jobs_service(
    redis: RedisClient = Depends(get_redis),
    api_client: APIClient = Depends(get_api_client),
    jobs_api: JobsAPI = Depends(get_jobs_api),
) -> JobsService:
    """
    Dependency for JobsService.
    Ensures that RedisClient, APIClient, and JobsAPI are injected properly.
    """
    return JobsService(redis_client=redis, api_client=api_client, jobs_api=jobs_api)
