from pydantic import BaseModel

# Dùng khi client gửi yêu cầu tạo bill
class BillDetailCreate(BaseModel):
    fruit_id: int
    weight: float

# Dùng khi trả về kết quả bill
class BillDetailResponse(BaseModel):
    detail_id: int
    fruit_id: int
    fruit_name: str | None
    weight: float
    price: float

    class Config:
        from_attributes = True
