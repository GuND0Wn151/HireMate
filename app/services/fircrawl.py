from app.api.request_utils import Normalizer
from app.core import redis_client
from app.core.redis_client import RedisClient
from app.core.consts import Consts


class FirecrawlService:
    def __init__(self, redis_client: RedisClient = None, ):
        self.redis_client = redis_client

    def upsert_job_description(self, url: str = ''):
        pass
    
    def extract_job(self, fingerprint: str):
        if self.redis_client.checkJobData(fingerprint):
            return self.redis_client.hget(fingerprint)
        



    def check_redis(self, fingerprint: str):
        pass
    
    def _job_description_fingerprint(self, url: str):
        normalized_url = Normalizer.norm_url(url)
         

