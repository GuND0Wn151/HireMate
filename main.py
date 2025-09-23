import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import job
# from infra.db.client import init_pool, close_pool
# from app.services.db_setup import ensure_users_table
# print(ensure_users_table())
def create_app() -> FastAPI:
	app = FastAPI(title="JobPrep AI Backend", version="1.0.0")

	# CORS for local dev; tighten in production
	allowed_origins = os.getenv("ALLOWED_ORIGINS", "*")
	origins = [o.strip() for o in allowed_origins.split(",") if o.strip()]
	app.add_middleware(
		CORSMiddleware,
		allow_origins=origins if origins else ["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	# Routers
	app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
	app.include_router(job.router, prefix="/api/job", tags=["job"])

	@app.get("/health")
	def health_check():
		return {"status": "ok"}

	return app

app = create_app()
