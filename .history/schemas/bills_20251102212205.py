from pydantic import BaseModel
from typing import List
from schemas.bill_details import BillDetailResponse
from schemas.customer import CustomerCreate

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

class BillDetailResponse(BaseModel):
    detail_id: int
    fruit_id: int
    fruit_name: Optional[str] = None  # Cho phép None nếu truy vấn thất bại
    weight: float
    price: float

    class Config:
        from_attributes = True