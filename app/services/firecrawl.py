from os import waitpid
from app.api.request_utils import Normalizer
from app.core.redis_client import RedisClient
from app.core.consts import Consts as prompts
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from app.core.fire_crawl import fetch_markdown 
from app.core.config import settings
from google import genai
from app.schemas.job import GeminiResponse



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
        print(url)
        markdown = fetch_markdown(url)
        self.organise_markdown(markdown)

    def check_redis(self, fingerprint: str): 
        pass
    
    def _job_description_fingerprint(self, url: str):
        normalized_url = Normalizer.norm_url(url)
         

    def organise_markdown(self, markdown_content: str):
        print('before gemini')

        # ensure configured earlier or do it here:
        client = genai.Client(api_key='AIzaSyD1GEIK9sXyMztOeWn62Fv3ANe3d6u5V6o')
        print('after making client')

        prompt = prompts.extract_job_v2(markdown_content)
        print('markdown')
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": GeminiResponse,
            },
        )
        print('after generate_content')
        print(response.text)

        return response

