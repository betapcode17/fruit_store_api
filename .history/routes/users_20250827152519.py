import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import User
from database import get_db
from schemas.users import UserCreate,UserUpdate,UserResponse
from passlib.context import CryptContext

router = APIRouter(
    tags=["Users"]
)

# security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# register
@router.post("Register",response_model= UserResponse)
def register(user_in:UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=404, detail=" Email Already register")
    
    hashed_pw = pwd_context.hash(user_in.password)
    


    user = User(**user_in.dict(exclude={"password"}),password = hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#login
@router.post("login",response_model=UserResponse)
def login(user_in: UserResponse, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not pwd_context.verify(user_in.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return user
     
#view profile
@router.get("/profile/{user_id}",response_model= UserResponse)
def view_profile(user_id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code= 404, detail= "User not found")
    return user


#view all profile
@ro

#update profile


# change pass