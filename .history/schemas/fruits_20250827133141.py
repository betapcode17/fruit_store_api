from pydantic import BaseModel
from typing import Optional

class FruitBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class FruitCreate(FruitBase):
    pass

class FruitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class FruitResponse(FruitBase):
    id: int

    class Config:
        orm_mode = True
