from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from app.core.deps import get_deps
from app.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.schemas import RegisterSchema, LoginSchema
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/signup")
async def signup(payload: RegisterSchema, db: AsyncSession = Depends(get_deps())):
	auth_service = AuthService(db)
	try:
		token_response = await auth_service.signup(payload.email, payload.password)
		return token_response
	except ValueError as ve:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
	except IntegrityError:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

@router.post("/login")
def login(payload: LoginSchema):
	# TODO: Implement with Supabase Auth or Clerk
	return {"message": "login stub", "email": payload.email}


