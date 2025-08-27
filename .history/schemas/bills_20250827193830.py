from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from .bill_details import BillDetailResponse


class BillItem(BaseModel):
    fruit_id: int
    weight: float


class BillCreate(BaseModel):
    user_id: int
    bill_id : int
    items: List[BillItem]


class BillResponse(BaseModel):
    bill_id: int
    date: Optional[date]
    user_id: int
    total_cost: float
    bill_details: List[BillDetailResponse] = []

    class Config:
        orm_mode = True
