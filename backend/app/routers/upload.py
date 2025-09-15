from fastapi import APIRouter, UploadFile, File, Form


router = APIRouter()


@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
	# TODO: parse PDF/DOCX to text, store in Supabase Storage
	return {"message": "resume upload stub", "filename": file.filename}


@router.post("/job")
async def upload_job(text: str = Form(...)):
	# TODO: parse JD text, extract skills
	return {"message": "job upload stub", "length": len(text)}


