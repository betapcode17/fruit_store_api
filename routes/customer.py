from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_
from database import get_db
from models import Customer
from schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)


# GET /customer/{cus_id} 
@router.get("/{cus_id}", response_model=CustomerResponse)
async def view_customer(cus_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.cus_id == cus_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# GET /customer — Xem tất cả khách hàng
@router.get("/", response_model=List[CustomerResponse])
async def view_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers



# POST /customer — Thêm khách hàng
@router.post("/", response_model=CustomerResponse)
async def create_customer(cus_in: CustomerCreate, db: Session = Depends(get_db)):
    # Kiểm tra trùng số điện thoại (nếu bạn có UNIQUE(phone))
    existing = db.query(Customer).filter(Customer.phone == cus_in.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    customer = Customer(**cus_in.dict())
    db.add(customer)
    db.commit()             
    db.refresh(customer)
    return customer



# PUT /customer/{cus_id} — Cập nhật thông tin khách hàng
@router.put("/{cus_id}", response_model=CustomerResponse)
async def update_cus(cus_id: int, cus_in: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.cus_id == cus_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in cus_in.dict(exclude_unset=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer


# GET /customer/search?keyword=... — Tìm kiếm khách hàng
@router.get("/search/{phone}", response_model=List[CustomerResponse])
async def search_customer(phone: str, db: Session = Depends(get_db)):
    customers = (
        db.query(Customer)
        .filter(Customer.phone.ilike(f"%{phone}%"))  # tìm theo chuỗi con trong số điện thoại
        .all()
    )

    if not customers:
        raise HTTPException(status_code=404, detail="No customer found")

    return customers
