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
    user = User(**user_in.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#login


#view profile


#view all profile


#update profile


# change pass