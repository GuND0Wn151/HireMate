from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.repos.users import UserRepository
from app.db.models.user import User
from app.schemas.auth import LoginSchema, RegisterSchema, UserSchema, AdditionalInfoSchema, TokenResponse, UserResponse,SignupResponse
from app.core.jwt_utils import jwt_manager
from sqlalchemy.exc import IntegrityError

class AuthService:
      def __init__(self, db: AsyncSession):
            self.user_repo = UserRepository(db)

      async def signup(self, email: str, password: str, name: str) -> SignupResponse:
            """
            Register a new user with email, password, and name.
            Returns success message upon successful registration.
            """
            # Check if user already exists
            existing_user = await self.user_repo.get_user_by_email(email)
            if existing_user:
                  raise ValueError("Email already registered")
            
            # Hash the password securely
            hashed_password = jwt_manager.get_password_hash(password)
            
            # Create new user
            new_user = User(
                  email=email, 
                  hashed_password=hashed_password,
                  username=name  # Store name in username field for now
            )
            
            try:
                  created_user = await self.user_repo.create_user(new_user)
                  
                  return {
                        "message": "User created successfully",
                        "user_id": created_user.id,
                        "email": created_user.email
                  }
            except IntegrityError:
                  raise ValueError("Email already registered")

      async def login(self, email: str, password: str) -> TokenResponse:
            """
            Authenticate user with email and password.
            Returns a JWT token upon successful authentication.
            """
            # Get user by email
            user = await self.user_repo.get_user_by_email(email)
            if not user:
                  raise ValueError("Invalid email or password")
            
            # Verify password
            if not jwt_manager.verify_password(password, user.hashed_password):
                  raise ValueError("Invalid email or password")
            
            # Check if user is active
            if not user.is_active:
                  raise ValueError("Account is deactivated")
            
            # Generate JWT token
            token = jwt_manager.create_user_token(user.id, user.email)
            
            return TokenResponse(
                  access_token=token,
                  token_type="bearer",
                  message="Login successful"
            )

      async def get_user_by_id(self, user_id: int) -> Optional[User]:
            """Get user by ID."""
            return await self.user_repo.get_user_by_id(user_id)



            