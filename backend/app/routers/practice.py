from fastapi import APIRouter
from typing import Optional


router = APIRouter()


@router.get("/request")
def request_problem(topic: Optional[str] = None, difficulty: Optional[str] = None):
	# TODO: fetch random problem from PracticeProblems with optional filters
	return {
		"id": 1,
		"title": "Two Sum (stub)",
		"topic": topic or "arrays",
		"difficulty": difficulty or "easy",
		"description": "Given an array ...",
	}


