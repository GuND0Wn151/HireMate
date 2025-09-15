from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
	app = FastAPI(title="JobPrep AI Backend", version="1.0.0")

	# CORS for local dev; tighten in production
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	# Routers
	from app.routers import auth, upload, resume, questions, practice, applications
	app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
	app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
	app.include_router(resume.router, prefix="/api", tags=["resume"])
	app.include_router(questions.router, prefix="/api/questions", tags=["questions"])
	app.include_router(practice.router, prefix="/api/practice", tags=["practice"])
	app.include_router(applications.router, prefix="/api/applications", tags=["applications"])

	@app.get("/health")
	def health_check():
		return {"status": "ok"}

	return app


app = create_app()


