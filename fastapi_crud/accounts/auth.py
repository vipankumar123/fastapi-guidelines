from fastapi import APIRouter,Depends
from .api import *
import schemas
from database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# register user end point
@auth_router.post("/register/user/",response_model=schemas.UserCreate, tags=["Authentication"])
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    data =  create_user(db=db, user=user)
    return data

@auth_router.post("/login", tags=["Authentication"])
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=form_data.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Username not found!!")
    if verify_password(form_data.password, db_user.hashed_password):
        token = create_access_token(db_user)
        return {"token": token, "token_type": "bearer"}
    return HTTPException(status_code=400, detail="password not matched!!")
