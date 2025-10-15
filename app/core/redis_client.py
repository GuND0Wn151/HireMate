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

        #set expiry to 1 month
        self.expiry = 30 * 24 * 3600  # 30 days in seconds
    
    def hset(self, key: str, mapping: dict):
        self.client.hset(key, mapping=mapping)

    def hget(self, key: str):
        return self.client.hget(key)
    
    def hgetAll(self, key: str):
        return self.client.hgetall(key)

    # make this generic and remove the hardcoded strings
    def addIndex(self, key: str):
        self.client.sadd("jobs:indices", key)

    def checkIndex(self, key: str) -> bool: 
        return self.client.sismember("jobs:indices", key)
        
    def isEmtpy(self, key: str) -> bool:
        return self.client.scard(key) == 0
        
    def check_redis_connection(self) -> bool:
        try:
            print('Checking Redis connection...')
            self.client.ping()
            return True
        except redis.ConnectionError:
            return False

    def addIndexExtract(self, key: str):
        self.client.sadd("jobs:details", key)
    
    def checkJobData(self, key: str):
        return self.client.sismember("jobs:details", key)
