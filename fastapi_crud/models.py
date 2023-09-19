from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    username = Column(String, unique=True)

    # Relationship with Skills
    skills = relationship("Skills", back_populates="user")

class Skills(Base):
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    skill_name = Column(String)

    # Foreign key relationship to users
    user_id = Column(Integer, ForeignKey("users.id"))

    # Establish the relationship with the User model
    user = relationship("User", back_populates="skills")
