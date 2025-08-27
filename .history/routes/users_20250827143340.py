import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import User
from database import get_db
from schemas.users import UserCreate,UserUpdate,UserResponse


router = APIRouter(
    prefix="/users"
    tags=["Users"]
)

# register
@router.post("")

#login


#view profile


#view all profile


#update profile


# change pass