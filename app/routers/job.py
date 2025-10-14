from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from typing import Optional
from app.core.config import settings
from app.schemas.job import ExtractRequest, ExtractResponse, PDFUploadResponse
from app.core.fire_crawl import fetch_markdown
from app.core.s3_utils import s3_service
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import os
from app.services.job_api import JobAPI
from app.core.consts import Consts




router = APIRouter()

@router.post("/extract-job", response_model=ExtractResponse)
async def extract_job_description(payload: ExtractRequest):
      try:
            # Scrape content as markdown for maximum extraction reliability
            markdown_content: Optional[str] = None
            try:
                  markdown_content = fetch_markdown(str(payload.url))
            except Exception:
                  markdown_content = None

            if not markdown_content:
                  raise HTTPException(status_code=502, detail="Failed to retrieve page content")

            # Use LangChain with OpenAI to extract and summarize job description
            try:
                  # Initialize OpenAI chat model with stricter parameters
                  llm = ChatOpenAI(
                        openai_api_key=settings.OPENAI_API_KEY,
                        model_name="gpt-5-nano",  # Use reliable model
                        temperature=0.1,  # Slightly more creative for better extraction
                        max_tokens=800  # Allow more comprehensive response
                  )
                  
                  # Create prompt for job description extraction and summarization
                  prompt = f"""
                  Extract ONLY the job description from the following job posting and format it as bullet points.
                  
                  EXTRACT ONLY:
                  - Job title and role
                  - Key responsibilities and duties
                  - Required qualifications and experience
                  - Required skills and technologies
                  - Preferred qualifications (if any)
                  
                  IGNORE COMPLETELY:
                  - Browser compatibility messages
                  - Company descriptions and boilerplate
                  - Benefits and perks information
                  - Application instructions
                  - Location details beyond what's essential
                  - Navigation elements or UI text
                  - Any text starting with "Sorry" or browser-related content
                  - Google Maps or cookie-related text
                  
                  FORMAT:
                  - Use bullet point format (• or -)
                  - Keep each bullet point concise but clear
                  - Focus on job-specific information only
                  
                  Job posting content:
                  {markdown_content}
                  
                  Return ONLY the clean job description in bullet points, nothing else.
                  """
                  
                  # Generate job description using LangChain
                  messages = [HumanMessage(content=prompt)]
                  response = llm.invoke(messages)
                  raw_response = response.content.strip()
                  
                  # Post-process to ensure we get exactly what we want
                  job_description = JobAPI._post_process_job_description(raw_response)
                  
            except Exception as e:
                  # Fallback to original markdown processing if LangChain fails
                  job_description = extract_job_description_from_markdown(markdown_content)

            return ExtractResponse(job_description=job_description, source_url=payload.url)
            
      except HTTPException:
            raise
      except Exception as e:
            raise HTTPException(status_code=500, detail=f"Job extraction error: {str(e)}")


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
