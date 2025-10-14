from os import waitpid
from app.api.request_utils import Normalizer
from app.core.redis_client import RedisClient
from app.core.consts import Consts as prompts
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from app.core.fire_crawl import fetch_markdown 
from app.core.config import settings

class FirecrawlService:
    def __init__(self, redis_client: RedisClient = None ):
        self.redis_client = redis_client

    def upsert_job_description(self, fingerprint: str = ''):
        self.redis_client.addIndexExtract(fingerprint)

        #prompts.get_extract_job()
    
    def extract_job(self, fingerprint: str):
        print('IN EXTRACT')
        if self.redis_client.checkJobData(fingerprint):
            return self.redis_client.hget(fingerprint) 
        print('after if') 
        url = self.redis_client.hgetAll(f'jobs:job:{fingerprint}')['apply_link']
        markdown = fetch_markdown(url)
        self.organise_markdown(markdown)

    def check_redis(self, fingerprint: str):
        pass
    
    def _job_description_fingerprint(self, url: str):
        normalized_url = Normalizer.norm_url(url)
         
    def organise_markdown(self, markdown_content:str):
        print('before llm')
        llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-5-nano",  # Use reliable model
            temperature=0.1,  # Slightly more creative for better extraction
            max_tokens=800  # Allow more comprehensive response
        )
        print('after llm')
        prompt = prompts.get_extract_job(markdown_content)
        messages = [HumanMessage(content=prompt)]
        response = llm.invoke(messages)
        print(" --------------- llm response -------------------")
        return response


