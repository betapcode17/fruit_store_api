from pydantic import BaseModel
from typing import Optional


class CustomerResponse(BaseModel):
    cus_id: int
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    moneySpent: float

    class Config:
        orm_mode = True  # để Pydantic tự động map từ SQLAlchemy model


# Schema để tạo khách hàng mới
class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    moneySpent: Optional[float] = 0


# Schema để cập nhật thông tin khách hàng
class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    moneySpent: Optional[float] = None
