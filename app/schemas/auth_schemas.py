from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class LoginSchema(BaseModel):
      email: EmailStr
      password: constr(min_length=6, max_length=100)

class RegisterSchema(BaseModel):
      email: EmailStr
      password: constr(min_length=6, max_length=100)
      name: constr(min_length=1, max_length=100)

class UserSchema(BaseModel):
      id: str
      email: EmailStr
      name: Optional[constr(min_length=1, max_length=100)] = None
      phno: Optional[constr(min_length=1, max_length=15)] = None
      company: Optional[constr(min_length=1, max_length=100)] = None
      role: Optional[constr(min_length=1, max_length=100)] = None

      class Config:
            orm_mode = True

class AdditionalInfoSchema(BaseModel):
      company: Optional[constr(min_length=1, max_length=100)] = None
      role: Optional[constr(min_length=1, max_length=100)] = None
      phno: Optional[constr(min_length=1, max_length=15)] = None
      username: Optional[constr(min_length=1, max_length=100)] = None

class TokenResponse(BaseModel):
      access_token: str
      token_type: str = "bearer"
      message: Optional[str] = "User created successfully"
      
class UserResponse(BaseModel):
      email: EmailStr
      message: Optional[str] = "User information updated successfully"\

class SignupResponse(BaseModel):
      message: Optional[str] = "User created successfully"
      user_id: Optional[int] = None
      email: Optional[EmailStr] = None