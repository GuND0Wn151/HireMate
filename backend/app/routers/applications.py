from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date


router = APIRouter()


class ApplicationCreate(BaseModel):
	company: str
	role: str
	status: str
	applied_date: date


@router.post("")
def add_application(payload: ApplicationCreate):
	# TODO: persist to Applications table
	return {"message": "application added (stub)", "company": payload.company}


@router.get("")
def list_applications():
	# TODO: fetch for current user
	return {"applications": []}


