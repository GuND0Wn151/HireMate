# dependency injection for FastAPI (get_db, get_redis, get_pinecone_client)

# get_db should return a session from sqlalchemy.orm.sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from .config import settings
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends

print("Creating async DB engine with settings:", settings.DATABASE_URL)
engine = create_async_engine(str(settings.DATABASE_URL), pool_size=settings.DB_MAX_SIZE, max_overflow=0)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
      async with SessionLocal() as session:
            try:
                  yield session
            except SQLAlchemyError as e:
                  print(f"Database error: {e}")
                  raise

def get_deps():
      return get_db