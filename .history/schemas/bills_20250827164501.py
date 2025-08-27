from pydantic import BaseModel
from typing import List

class BillItem(BaseModel):
    fruit_id: int
    quantity: float

class BillCreate(BaseModel):
    items: List[BillItem]

class BillDetailResponse(BaseModel):
    fruit_name: str
    quantity: float
    price: float

class BillResponse(BaseModel):
    id: int
    total: float
    details: list[BillDetailResponse]

    class Config:
        orm_mode = True
