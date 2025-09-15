from fastapi import APIRouter
from pydantic import BaseModel, EmailStr


router = APIRouter()


class SignUpRequest(BaseModel):
	name: str
	email: EmailStr
	password: str


class LoginRequest(BaseModel):
	email: EmailStr
	password: str


@router.post("/signup")
def signup(payload: SignUpRequest):
	# TODO: Implement with Supabase Auth or Clerk
	return {"message": "signup stub", "email": payload.email}


@router.post("/login")
def login(payload: LoginRequest):
	# TODO: Implement with Supabase Auth or Clerk
	return {"message": "login stub", "email": payload.email}


