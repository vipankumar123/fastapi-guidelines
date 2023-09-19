from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, create_tables
from models import Skills, User
from schemas import SkillSchema, SkillsCreate, UserSchema
from typing import List
from accounts import auth
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Security
from accounts.api import get_current_user
from accounts.api import get_user_by_username

f = get_user_by_username


app = FastAPI()

app.include_router(auth.auth_router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Create tables when the server starts
create_tables()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=List[UserSchema], tags=["Authentication"])
def get_all_users(db: Session = Depends(get_db), user: User = Security(get_current_user, scopes=["read"])):
    users = db.query(User).all()
    return users

# Define the route to get a user by ID
@app.get("/users/{user_id}", response_model=UserSchema, tags=["Authentication"])
def get_user_by_id(user_id: int, db: Session = Depends(get_db), user: User = Security(get_current_user)):
    # Retrieve the user from the database by user_id
    user = db.query(User).filter(User.id == user_id).first()
    
    # Check if the user exists
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return the user as a response
    return user

@app.post("/skills/", response_model=SkillSchema, tags=["Skills"])
def create_skill(
    skill: SkillsCreate,
    db: Session = Depends(get_db),
    user: User = Security(get_current_user, scopes=["create"]),
):
    skill = db.query(Skills).filter(Skills.id == skill.user_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill id not found")
    db_skill = Skills(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# Replace the route for reading a skill by ID
@app.get("/skills/{skill_id}", response_model=SkillSchema, tags=["Skills"])
def read_skill(skill_id: int, db: Session = Depends(get_db), user: User = Security(get_current_user)):
    skill = db.query(Skills).filter(Skills.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

# Replace the route for updating a skill by ID
@app.put("/skills/{skill_id}", response_model=SkillSchema, tags=["Skills"])
def update_skill(skill_id: int, updated_skill: SkillsCreate, db: Session = Depends(get_db), user: User = Security(get_current_user)):
    existing_skill = db.query(Skills).filter(Skills.id == skill_id).first()
    if existing_skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    for field, value in updated_skill.dict().items():
        setattr(existing_skill, field, value)

    db.commit()
    db.refresh(existing_skill)
    return existing_skill

# Replace the route for deleting a skill by ID
@app.delete("/skills/{skill_id}", response_model=SkillSchema, tags=["Skills"])
def delete_skill(skill_id: int, db: Session = Depends(get_db), user: User = Security(get_current_user)):
    skill = db.query(Skills).filter(Skills.id == skill_id).first()
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return skill

# Replace the route for getting all skills
@app.get("/skills/", response_model=List[SkillSchema], tags=["Skills"])
def get_all_skills(db: Session = Depends(get_db), user: User = Security(get_current_user)):
    skills = db.query(Skills).all()
    return skills


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
