from pydantic import BaseModel, AnyUrl
class ExtractRequest(BaseModel):
      url: AnyUrl


class ExtractResponse(BaseModel):
      job_description: str
      source_url: AnyUrl