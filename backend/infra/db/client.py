
from psycopg_pool import ConnectionPool
from .core.config import settings
from typing import Optional

_pool: Optional[ConnectionPool] = None

def init_pool() -> None:
    global _pool
    if _pool is None:
        # conninfo can be a DSN or key=value string
        _pool = ConnectionPool(conninfo=str(settings.DATABASE_URL),
                               min_size=settings.DB_MIN_SIZE,
                               max_size=settings.DB_MAX_SIZE)

def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None

def get_pool() -> ConnectionPool:
    if _pool is None:
        raise RuntimeError("Connection pool not initialized - call init_pool() on startup")
    return _pool
