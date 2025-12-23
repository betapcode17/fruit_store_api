from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.users import UserCreate, UserLogin, UserResponse
from passlib.context import CryptContext
from core.security import create_access_token

router = APIRouter(
    prefix="/user",
    tags=["Auth / Public"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = pwd_context.hash(user_in.password)
    user = User(**user_in.dict(exclude={"password"}), password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
async def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not pwd_context.verify(user_in.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if user.valid is False:
        raise HTTPException(status_code=403, detail="Account is banned")

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
        },
    }
