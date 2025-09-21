from sqlalchemy import String, Boolean, Column, text
from sqlalchemy import Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
      __tablename__ = "users"

      id = Column(
            Integer,
            primary_key=True,
            index=True,
            autoincrement=True
      )
      email = Column(String, unique=True, index=True, nullable=False)
      hashed_password = Column(String, nullable=False)
      company = Column(String, nullable=True)
      role = Column(String, nullable=True)
      username = Column(String, nullable=True)
      phno = Column(String, nullable=True)
      is_active = Column(Boolean, default=True)

      def __repr__(self) -> str:
            return f"<User(id={self.id}, email={self.email})>"

      def to_dict(self) -> dict:
            return {
                  "id": str(self.id),
                  "email": self.email,
                  "company": self.company,
                  "role": self.role,
                  "username": self.username,
                  "phno": self.phno,
                  "is_active": self.is_active,
            }