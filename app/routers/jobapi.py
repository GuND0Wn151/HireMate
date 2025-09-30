from app.services.jobs_service import JobsService
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app.core.deps import get_jobs_service

router = APIRouter()

@router.get("/jobs")
async def get_jobs(jobs_service: JobsService = Depends(get_jobs_service)):
      try:
            print('dd')
            jobs = jobs_service.get_jobs()
            return jobs
      except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))