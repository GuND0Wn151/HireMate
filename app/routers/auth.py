from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from app.core.deps import get_deps
from app.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import RegisterSchema, LoginSchema, UserSchema
from app.db.models.user import User
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/signup")
async def signup(payload: RegisterSchema, db: AsyncSession = Depends(get_deps())):
	"""
	Register a new user with email, password, and name.
	Returns a JWT token upon successful registration.
	"""
	auth_service = AuthService(db)
	try:
		token_response = await auth_service.signup(payload.email, payload.password, payload.name)
		return token_response
	except ValueError as ve:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
	except IntegrityError:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

@router.post("/login")
async def login(payload: LoginSchema, db: AsyncSession = Depends(get_deps())):
	"""
	Authenticate user with email and password.
	Returns a JWT token upon successful authentication.
	"""
	auth_service = AuthService(db)
	try:
		token_response = await auth_service.login(payload.email, payload.password)
		return token_response
	except ValueError as ve:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ve))


# Note: The /me endpoint has been removed since get_current_user dependency 
# was removed from deps.py. You can create a separate authentication module 
# if you need protected routes.


