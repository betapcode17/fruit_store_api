from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import Bill, BillDetail, Fruit, Customer
from schemas.bills import BillCreate, BillResponse
from schemas.bill_details import BillDetailResponse
from schemas.customer import CustomerResponse
from datetime import datetime
import pytz

router = APIRouter(tags=["Bills"])

# múi giờ Việt Nam
VN_TZ = pytz.timezone("Asia/Ho_Chi_Minh")

def to_vn_time(dt: datetime) -> str:
    if dt is None:
        return None
    dt_vn = dt.astimezone(VN_TZ)
    return dt_vn.strftime("%d-%m-%Y %H:%M:%S")


# ✅ POST /bill — thêm Bill và Customer
@router.post("/bill", response_model=BillResponse)
def create_bill(bill_in: BillCreate, db: Session = Depends(get_db)):
    total_cost = 0
    bill_details_list = []

    # 🔹 1. Tạo Customer mới
    customer_data = bill_in.customer
    new_customer = Customer(
        name=customer_data.name,
        phone=customer_data.phone,
        address=customer_data.address,
        moneySpent=0  # ban đầu = 0, sẽ cộng sau
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    # 🔹 2. Tạo Bill
    bill = Bill(
        user_id=bill_in.user_id,
        date=datetime.utcnow(),
        total_cost=0,
        cus_id=new_customer.cus_id  # gán customer ID cho hóa đơn
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)

    # 🔹 3. Thêm chi tiết Bill (BillDetail)
    for item in bill_in.items:
        fruit = db.query(Fruit).filter(Fruit.id == item.fruit_id).first()
        if not fruit:
            raise HTTPException(status_code=404, detail=f"Fruit ID {item.fruit_id} not found")

        price = fruit.price * item.weight
        total_cost += price

        detail = BillDetail(
            bill_id=bill.bill_id,
            fruit_id=item.fruit_id,
            weight=item.weight,
            price=fruit.price
        )
        db.add(detail)
        bill_details_list.append(detail)

    # 🔹 4. Cập nhật total_cost cho bill và customer.moneySpent
    bill.total_cost = total_cost
    new_customer.moneySpent += total_cost

    db.commit()
    for detail in bill_details_list:
        db.refresh(detail)

    # 🔹 5. Chuẩn bị dữ liệu trả về
    response_details = [
        BillDetailResponse(
            detail_id=d.detail_id,
            fruit_id=d.fruit_id,
            fruit_name=db.query(Fruit).filter(Fruit.id == d.fruit_id).first().name,
            weight=d.weight,
            price=d.price
        )
        for d in bill_details_list
    ]

    return BillResponse(
        bill_id=bill.bill_id,
        date=to_vn_time(bill.date),
        user_id=bill.user_id,
        total_cost=total_cost,
        bill_details=response_details
    )
