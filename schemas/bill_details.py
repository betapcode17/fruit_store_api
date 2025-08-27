from pydantic import BaseModel

class BillDetailResponse(BaseModel):
    detail_id: int
    fruit_id: int
    fruit_name: str   # tên quả lấy từ Fruit
    weight: float
    price: float

    class Config:
        orm_mode = True
