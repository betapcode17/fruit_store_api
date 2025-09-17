from pydantic import BaseModel
from typing import Optional
from datetime import date

class FruitCreate(BaseModel):
    name: str
    description: str
    quantity: int
    image: str
    price: float

class FruitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    image: Optional[str] = None
    price: Optional[float] = None

class FruitResponse(BaseModel):
    id: int
    name: str
    description: str
    quantity: int
    image: str
    price: float

    class Config:
        orm_mode = True
