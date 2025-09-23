from fastapi import APIRouter, HTTPException
from typing import Optional
from app.core.config import settings
from app.schemas.job import ExtractRequest, ExtractResponse
from app.core.fire_crawl import _get_firecrawl_client, fetch_markdown, extract_job_description_from_markdown

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


