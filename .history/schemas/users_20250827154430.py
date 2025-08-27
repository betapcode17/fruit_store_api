from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


# ----- CREATE -----
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: str
    address: str
    birth: date
    gender: bool
    username: str
    role: bool
    valid: bool


# ----- UPDATE -----
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth: Optional[date] = None
    gender: Optional[bool] = None
    username: Optional[str] = None
    role: Optional[bool] = None
    valid: Optional[bool] = None


# ----- RESPONSE -----
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    phone: str
    address: str
    birth: date
    gender: bool
    username: str
    role: bool
    valid: bool

    class Config:
        orm_mode = True


# ----- LOGIN -----
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ----- CHANGE PASSWORD -----
class ChangePassword(BaseModel):
    old_password: str
    new_password: str
