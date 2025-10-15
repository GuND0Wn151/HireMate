from pydantic import BaseModel, AnyUrl
from typing import Optional

class ExtractRequest(BaseModel):
    url: AnyUrl


class ExtractResponse(BaseModel):
    job_description: str
    source_url: AnyUrl


class PDFUploadResponse(BaseModel):
    file_url: str
    s3_key: str
    original_filename: str
    file_size: int
    upload_timestamp: str
    user_email: str
    email_prefix: str
    message: str = "PDF uploaded successfully"

class ListJobsResponse(BaseModel):
    count: int
    jobsList: list 

class JobMetaData(BaseModel):
    company_name: str
    location: str
    employment_type: str
    salary_range: Optional[str]

class GeminiResponse(BaseModel):
    job_title_and_role: str
    about_company: str
    key_responsibilities: str
    requirements: Optional[str]
    skill_and_technologies: Optional[str]
    preferred_qualifications: Optional[str]
    benefits_or_perks: Optional[str]
    job_metadata: JobMetaData



 
