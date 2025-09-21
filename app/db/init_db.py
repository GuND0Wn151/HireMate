from dotenv import load_dotenv
load_dotenv(".env")
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.models.user import Base  # adjust if your import path differs
import os

async def init_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable not set")
    engine = create_async_engine(DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(init_db())
