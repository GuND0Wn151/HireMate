import redis
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )

    def set(self, key: str, value: str, ex: int = 3600):
        """Set a value in Redis with an expiration time (default 1 hour)."""
        self.client.set(name=key, value=value, ex=ex)

    def get(self, key: str) -> str:
        """Get a value from Redis by key."""
        return self.client.get(name=key)

    def delete(self, key: str):
        """Delete a key from Redis."""
        self.client.delete(key)
