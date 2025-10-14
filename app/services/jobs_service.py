from app.core.redis_client import RedisClient
from app.api.api_client import APIClient
from app.api.jobs_api import JobsAPI
from app.schemas.job import ListJobsResponse

class JobsService:
      def __init__(self, redis_client: RedisClient = None, api_client: APIClient = None, jobs_api: JobsAPI = None):
            self.redis_client = redis_client
            self.api_client = api_client
            self.jobs_api = jobs_api
            self.redis_client.check_redis_connection()


      def get_jobs(self) -> ListJobsResponse:
            """Fetch jobs from JobAPI and store them in Redis."""
            # Check if jobs are already indexed
            print(self.redis_client.isEmtpy("jobs:indices"),' is empty')
            if self.redis_client.isEmtpy("jobs:indices"):
                  self._add_all_from_api()
            
            # Fetch all jobs from Redis
            all_jobs = []
            for index in self.redis_client.client.smembers("jobs:indices"):
                  job_data = self.redis_client.client.hgetall(f"jobs:job:{index}")
                  if job_data:
                        all_jobs.append(job_data)
        
            return ListJobsResponse(count=len(all_jobs), jobsList=all_jobs)
      
      def _upsert_job(self, job: dict):
            """Insert or update a job in Redis."""
            key = f"jobs:job:{job['fingertprint']}"
            self.redis_client.hset(key, mapping=job)

      def _add_job_index(self, index_name: str):
            """Add a new job index to Redis."""
            self.redis_client.addIndex(index_name)

      def _add_all_from_api(self) -> list:
            """Fetch all jobs from JobAPI and store them in Redis."""
            jobs = self.jobs_api.get_job_details()
            for job in jobs:
                  self._upsert_job(job)
                  self._add_job_index(job['fingertprint'])

            return jobs

