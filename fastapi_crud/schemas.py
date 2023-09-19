from pydantic import BaseModel
from datetime import datetime
from typing import List

class SkillsBase(BaseModel):
    skill_name: str

class SkillsCreate(SkillsBase):
    user_id: int  # Use colon instead of equals sign

class SkillSchema(SkillsBase):
    id: int
    user_id: int  # Use colon instead of equals sign

class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active : bool

class UserSchema(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active : bool
    skills : List[SkillSchema]
