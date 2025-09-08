from pydantic import BaseModel
from datetime import date
from typing import Optional

# Doanh thu theo ngày
class RevenueDay(BaseModel):
    day: date
    total_revenue: float

# Doanh thu theo tháng
class RevenueMonth(BaseModel):
    year: int
    month: int
    total_revenue: float

# Top fruit
class TopFruit(BaseModel):
    name: str
    total_weight: float
    revenue: float

# Doanh thu theo loại trái cây
class RevenueFruit(BaseModel):
    name: str
    total_revenue: float
