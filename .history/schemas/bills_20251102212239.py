from pydantic import BaseModel
from typing import List
from schemas.bill_details import BillDetailResponse
from schemas.customer import CustomerCreate

from typing import Optional
class BillCreate(BaseModel):
    user_id: int
    customer: CustomerCreate
    items: List[BillDetailResponse]

class BillResponse(BaseModel):
    bill_id: int
    date: str
    user_id: int
    total_cost: float
    bill_details: List[BillDetailResponse]

    class Config:
        from_attributes = True

