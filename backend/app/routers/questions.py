from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional


router = APIRouter()


class QuestionGenRequest(BaseModel):
	job_description_id: Optional[str] = None
	text: Optional[str] = None


@router.post("/generate")
def generate_questions(payload: QuestionGenRequest):
	# TODO: Call OpenAI to generate 5-10 questions and persist
	return {"questions": ["Tell me about yourself (stub)"]}


