from pydantic import BaseModel
from typing import Optional

class CustomerResponse(BaseModel):
    cus_id: int
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    moneySpent: float = 0.0

    class Config:
        orm_mode = True  # Cho phép tự động map từ SQLAlchemy model


class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    moneySpent: Optional[float] = 0.0


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    moneySpent: Optional[float] = None
