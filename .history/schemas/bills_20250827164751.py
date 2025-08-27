from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class BillItem(BaseModel):
    fruit_id: int
    quantity: float


class BillCreate(BaseModel):
    user_id: int
    items: List[BillItem]


# Hóa đơn trả về
class BillResponse(BaseModel):
    bill_id: int
    date: Optional[date]
    user_id: int
    total_cost: float
   

    class Config:
        orm_mode = True
