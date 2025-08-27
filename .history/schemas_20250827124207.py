from pydantic import BaseModel
from typing import Optional
from datetime import date

class FruitCreate(BaseModel):
    name: str
    description: str
    exist: bool
    image: str
    price: float

class FruitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    exist: Optional[bool] = None
    image: Optional[str] = None
    price: Optional[float] = None

class FruitResponse(BaseModel):
    id: int
    name: str
    description: str
    exist: bool
    image: str
    price: float

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email:str
    password:str
    name: str
    phone: str
    address: str
    birth:date
    gender:bool
    username: str
    role: bool
    valid:bool


class UserUpdate(BaseModel):
    email:Optional[str] = None
    password:Optional[str] = None
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth:Optional[date] = None
    gender:Optional[bool] = None
    username: Optional[str] = None
    role: Optional[bool] = None
    valid:Optional[bool] = None



class UserCreate(BaseModel):
    email:str
    password:str
    name: str
    phone: str
    address: str
    birth:date
    gender:bool
    username: str
    role: bool
    valid:bool

    class  Config:
        orm_mode = True