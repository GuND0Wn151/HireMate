from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.repos.users import UserRepository
from app.db.models.user import User
from app.auth.schemas import LoginSchema, RegisterSchema, UserSchema, AdditionalInfoSchema, TokenResponse, UserResponse

class AuthService:
      def __init__(self, db: AsyncSession):
            self.user_repo = UserRepository(db)
      
      def hash_password(self, password: str) -> str:
            # Implement a secure password hashing mechanism here
            import hashlib
            return hashlib.sha256(password.encode()).hexdigest()

      async def signup(self, email: str, password: str) -> TokenResponse:
            existing_user = await self.user_repo.get_user_by_email(email)
            if existing_user:
                  raise ValueError("Email already registered")
            hashed_password = self.hash_password(password)
            new_user = User(email=email, hashed_password=hashed_password)
            created_user = await self.user_repo.create_user(new_user)
            # todo: generate JWT token
            token = "dummy_token"  # Replace with actual token generation logic
            return TokenResponse(
                  access_token=token,
                  message="User created successfully",
            )
      

      async def login(self, email: str, password: str) -> TokenResponse:
            # todo: implement login logic with password verification and token generation
            pass



            