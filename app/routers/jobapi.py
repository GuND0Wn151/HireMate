from app.services.jobs_service import JobsService
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.core.deps import get_firecrawl_service, get_jobs_service
from app.schemas.job import ListJobsResponse  
from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from typing import Optional
from app.core.config import settings
from app.schemas.job import ExtractRequest, ExtractResponse, PDFUploadResponse
from app.core.fire_crawl import _get_firecrawl_client, fetch_markdown
from app.core.s3_utils import s3_service
from app.services.fircrawl import FirecrawlService

router = APIRouter()

@router.get("/list")
async def get_jobs(jobs_service: JobsService = Depends(get_jobs_service)) -> ListJobsResponse: 

    """
    Get the list of jobs in the list page, this stores data in redis first and retrives
    """
    try:
        return jobs_service.get_jobs()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/{job_id}", response_model=ExtractResponse)
async def extract_job_description(job_id, firecrawl_service: FirecrawlService = Depends(get_firecrawl_service)):
    """
    get detailed information about job, done using job fingerprint.
    we get data from firecrawl and cache it.
    """
    try:
        fingerprint = job_id
        data = firecrawl_service.extract_job(fingerprint)
        return data
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
