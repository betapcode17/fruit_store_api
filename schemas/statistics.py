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
