from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.users import UserResponse, UserUpdate, ChangePassword
from core.security import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"],
  
)


@router.get("/me", response_model=UserResponse)
async def read_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/", response_model=list[UserResponse])
async def view_all_profiles(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.put("/profile/{user_id}", response_model=UserResponse)
async def update_profile(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_in.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


@router.put("/profile/{user_id}/change-password")
async def change_password(user_id: int, data: ChangePassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Old password incorrect")

    user.password = pwd_context.hash(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

@router.get("/profile/{user_id}", response_model=UserResponse)
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}/ban")
async def ban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.valid = False
    db.commit()

    return {"message": "User has been banned"}

@router.put("/{user_id}/active")
async def active_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.valid = True
    db.commit()

    return {"message": "User has been activated"}

