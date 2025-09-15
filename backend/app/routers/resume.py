from fastapi import APIRouter


router = APIRouter()


@router.get("/resume/{resume_id}/similarity")
def similarity(resume_id: str, jobId: str):
	# TODO: compute embedding similarity + ATS feedback
	return {
		"resumeId": resume_id,
		"jobId": jobId,
		"similarity": 0.0,
		"missingKeywords": [],
	}


