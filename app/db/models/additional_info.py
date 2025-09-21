from sqlalcheymy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .user import User

class Preferences(Base):
      __tablename__ = "preferences"

      id = Column(Integer, primary_key=True, index=True, autoincrement=True)
      user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
      preference_data = Column(String, nullable=True)
      

      user = relationship("User", back_populates="preferences")