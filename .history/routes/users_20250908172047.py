from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas.users import UserCreate, UserResponse, UserUpdate, UserLogin, ChangePassword
from passlib.context import CryptContext

router = APIRouter(
     tags=["User"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------- REGISTER --------
@router.post("/register", response_model=UserResponse)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # check email tồn tại chưa
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # mã hoá mật khẩu
    hashed_pw = pwd_context.hash(user_in.password)
    user = User(**user_in.dict(exclude={"password"}), password=hashed_pw)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# -------- LOGIN --------
@router.post("/login", response_model=UserResponse)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not pwd_context.verify(user_in.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return user


# -------- VIEW PROFILE --------
@router.get("/profile/{user_id}", response_model=UserResponse)
def view_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------- VIEW ALL PROFILES --------
@router.get("/profiles", response_model=list[UserResponse])
def view_all_profiles(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# -------- UPDATE PROFILE --------
@router.put("/profile/{user_id}", response_model=UserResponse)
def update_profile(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_in.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user



# -------- DELETE USER --------
@router.delete("/profile/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# -------- CHANGE PASSWORD --------
@router.put("/profile/{user_id}/change-password")
def change_password(user_id: int, data: ChangePassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.password = pwd_context.hash(data.new_password)
    db.commit()
    return {"message": "Password updated successfully"}

# -------- BAN ACC--------