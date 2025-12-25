from pydantic import BaseModel
from datetime import date
from typing import Optional

class RevenueDay(BaseModel):
    day: date
    total_revenue: float

class RevenueMonth(BaseModel):
    year: int
    month: int
    total_revenue: float

class TopFruit(BaseModel):
    name: str
    total_weight: float
    revenue: float

class RevenueFruit(BaseModel):
    name: str
    total_revenue: float

class TopSeller(BaseModel):
    user_id: int
    name: str
    total_revenue: float

    class Config:
        from_attributes = True

class TopCustomer(BaseModel):
    cus_id: int
    name: str
    phone: str
    moneySpent: float

    class Config:
        from_attributes = True
