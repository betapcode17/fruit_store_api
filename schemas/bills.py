from pydantic import BaseModel
from typing import List, Optional
from schemas.bill_details import BillDetailCreate, BillDetailResponse

class BillCreate(BaseModel):
    user_id: int
    cus_id: Optional[int] = None
    items: List[BillDetailCreate]

class BillResponse(BaseModel):
    bill_id: int
    date: str
    user_id: int
    cus_id: Optional[int] = None   # ✅ SỬA Ở ĐÂY
    total_cost: float
    bill_details: List[BillDetailResponse]

    class Config:
        from_attributes = True
