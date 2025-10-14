from pydantic import BaseModel, AnyUrl


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






  
