from pydantic import BaseModel

class BillDetailResponse(BaseModel):
    detail_id: int
    fruit_id: int
    fruit_name: str
    weight: float
    price: float

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