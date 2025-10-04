from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from typing import Optional
from app.core.config import settings
from app.schemas.job import ExtractRequest, ExtractResponse, PDFUploadResponse
from app.core.fire_crawl import _get_firecrawl_client, fetch_markdown, extract_job_description_from_markdown
from app.core.s3_utils import s3_service

router = APIRouter()








@router.post("/extract-job", response_model=ExtractResponse)
async def extract_job_description(payload: ExtractRequest):
      client = _get_firecrawl_client()
      try:
            # Scrape content as markdown for maximum extraction reliability
            markdown_content: Optional[str] = None
            try:
                  markdown_content = fetch_markdown(str(payload.url))
            except Exception:
                  markdown_content = None

            job_description = None

            # Try Firecrawl extract with a focused prompt
            try:
                  extract_result = client.extract(
                        [str(payload.url)],
                        prompt=(
                              "Extract ONLY the job description text from this page. "
                              "Do not include company boilerplate, application instructions, or unrelated sections. "
                              "Return plain text."
                        ),
                  )
                  if getattr(extract_result, "success", False):
                        # Some SDKs return a list of dicts in data; fall back to markdown if missing
                        data = getattr(extract_result, "data", None)
                        if isinstance(data, list) and data:
                              first = data[0]
                              if isinstance(first, dict):
                                    # Prefer 'job_description' key if present; else join values
                                    job_description = (
                                          first.get("job_description")
                                          or first.get("content")
                                          or None
                                    )
            except Exception:
                  # Ignore extract errors; we'll fall back to markdown
                  pass

            if not job_description:
                  # Fallback: use markdown content, then post-process to isolate JD
                  if not markdown_content:
                        raise HTTPException(status_code=502, detail="Failed to retrieve page content")
                  job_description = extract_job_description_from_markdown(markdown_content)

            return ExtractResponse(job_description=job_description.strip(), source_url=payload.url)
      except HTTPException:
            raise
      except Exception as e:
            raise HTTPException(status_code=500, detail=f"Firecrawl error: {str(e)}")


@router.post("/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(
    file: UploadFile = File(..., description="PDF file to upload"),
    user_email: str = Form(..., description="User email for file organization (required)")
):
    """
    Upload a PDF file to AWS S3 using multipart form data
    
    Args:
        file: The PDF file to upload (multipart form data)
        user_email: User email for organizing files in folders (uses part before @)
        
    Returns:
        PDFUploadResponse: Upload details including file URL and metadata
    """
    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(
                status_code=400, 
                detail="No file provided"
            )
        
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400, 
                detail="Only PDF files are allowed"
            )
        
        # Validate file size (e.g., 10MB limit)
        file_content = await file.read()
        max_file_size = 10 * 1024 * 1024  # 10MB
        if len(file_content) > max_file_size:
            raise HTTPException(
                status_code=413, 
                detail="File size exceeds 10MB limit"
            )
        
        if len(file_content) == 0:
            raise HTTPException(
                status_code=400, 
                detail="Empty file provided"
            )
        
        # Upload to S3
        upload_result = await s3_service.upload_pdf(
            file_content=file_content,
            original_filename=file.filename,
            user_email=user_email
        )
        
        return PDFUploadResponse(**upload_result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to upload PDF: {str(e)}"
        )
