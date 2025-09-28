from app.api.request_utils import DeNormalizer, Normalizer, HashUtils
from app.api.api_client import APIClient
from app.core.redis_client import RedisClient
from hashlib import sha256

redis_client = RedisClient()
api_client = APIClient()

class JobsAPI:
      @staticmethod
      def get_job_details(job_id: str) -> dict:
            """Fetch job details from JobAPI and normalize the data."""
            url = f"https://api.jobapi.dev/v1/jobs/{job_id}"
            headers = {"Authorization : Bearer YOUR_API_KEY"}
            job_data = api_client.get(url, headers=headers)

            all_jobs = []
            job_attributes = ["id", "title", "company", "location", "posted_date", "job_description", "apply_link", "job_title"]
            for i in job_data:
                  job = {}
                  for attr in job_attributes:
                        if attr in i:
                              if attr in ["title", "company", "job_description", "job_title"]:
                                    job[attr] = DeNormalizer.denorm_text(i[attr])
                              elif attr == "location":
                                    job[attr] = DeNormalizer.denorm_location(i[attr])
                              elif attr == "posted_date":
                                    job[attr] = DeNormalizer.denorm_date(i[attr])
                              elif attr == "apply_link":
                                    job[attr] = DeNormalizer.denorm_url(i[attr])
                              else:
                                    job[attr] = i[attr]
                  all_jobs.append(job)
            
            return all_jobs

      @staticmethod
      def fingerprint_job(job: dict) -> str:
            """Generate a unique fingerprint for a job posting."""
            fp_payload = {
                  "title": job.get("job_title") or job.get("title"),
                  "company": job.get("company"),
                  "location": job.get("location"),
                  "job_description": job.get("job_description"),
                  "apply_link": job.get("apply_link"),
                  "date_posted": job.get("posted_date"),
            }

            return HashUtils.fingerprint(fp_payload)


