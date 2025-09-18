from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from typing import Optional

from app.db.models.user import User

class UserRepository:
      def __init__(self, db: AsyncSession):
            self.db = db

      async def get_user_by_email(self, email: str) -> Optional[User]:
            result = await self.db.execute(select(User).where(User.email == email))
            return result.scalars().first()

      async def create_user(self, user: User) -> User:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user

      async def update_user_info(self, user_id: str, company: Optional[str] = None,
                                 role: Optional[str] = None, phno: Optional[str] = None,
                                 username: Optional[str] = None) -> Optional[User]:
            stmt = update(User).where(User.id == user_id)
            if company is not None:
                  stmt = stmt.values(company=company)
            if role is not None:
                  stmt = stmt.values(role=role)
            if phno is not None:
                  stmt = stmt.values(phno=phno)
            if username is not None:
                  stmt = stmt.values(username=username)

            stmt = stmt.returning(User)
            result = await self.db.execute(stmt)
            await self.db.commit()
            return result.scalars().first()