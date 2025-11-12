from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
import pytz
import shutil
from database import get_db
from models import Bill, BillDetail, Fruit, Customer
from schemas.bills import BillCreate, BillResponse
from schemas.bill_details import BillDetailResponse
from schemas.customer import CustomerResponse
import os, json, glob, re
router = APIRouter(tags=["Bills"])

import shutil

@router.post("/bill", response_model=BillResponse)
def create_bill(bill_in: BillCreate, db: Session = Depends(get_db)):
    total_cost = 0
    bill_details_list = []

    # 1️⃣ Kiểm tra Customer tồn tại
    customer = db.query(Customer).filter(Customer.cus_id == bill_in.cus_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer ID {bill_in.cus_id} not found")

    # 2️⃣ Tạo Bill mới
    bill = Bill(
        user_id=bill_in.user_id,
        date=datetime.utcnow(),
        total_cost=0,
        cus_id=bill_in.cus_id
    )
    db.add(bill)
    db.commit()
    db.refresh(bill)

    # 3️⃣ Thêm chi tiết Bill
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

    # 4️⃣ Cập nhật tổng tiền
    bill.total_cost = total_cost
    customer.moneySpent += total_cost
    db.commit()

    for d in bill_details_list:
        db.refresh(d)

    # 5️⃣ Chuẩn bị dữ liệu trả về
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

    # 6️⃣ ✅ Xóa toàn bộ file trong thư mục json_results và uploads sau khi tạo bill thành công
    JSON_DIR = "json_results"
    UPLOAD_DIR = "uploads"

    for folder in [JSON_DIR, UPLOAD_DIR]:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return BillResponse(
        bill_id=bill.bill_id,
        date=str(bill.date),
        user_id=bill.user_id,
        cus_id=bill.cus_id,
        total_cost=total_cost,
        bill_details=response_details
    )

#  GET /ViewAllBill — xem tất cả hóa đơn
@router.get("/ViewAllBill", response_model=List[BillResponse])
def view_all_bills(db: Session = Depends(get_db)):
    bills = db.query(Bill).all()
    all_bills = []

    for bill in bills:
        details = []
        for d in bill.bill_details:
            fruit = db.query(Fruit).filter(Fruit.id == d.fruit_id).first()
            details.append(
                BillDetailResponse(
                    detail_id=d.detail_id,
                    fruit_id=d.fruit_id,
                    fruit_name=fruit.name if fruit else None,  # tránh lỗi NoneType
                    weight=d.weight,
                    price=d.price
                )
            )

        all_bills.append(
            BillResponse(
                bill_id=bill.bill_id,
                date=str(bill.date),  # chỉ cần chuyển sang string
                user_id=bill.user_id,
                cus_id= bill.cus_id,
                total_cost=bill.total_cost,
                bill_details=details
            )
        )

    return all_bills



#  PUT /bill/{bill_id} — cập nhật hóa đơn
@router.put("/bill/{bill_id}", response_model=BillResponse)
def update_bill(bill_id: int, bill_in: BillCreate, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    # Xóa chi tiết cũ
    db.query(BillDetail).filter(BillDetail.bill_id == bill_id).delete()
    db.commit()

    total_cost = 0
    bill_details_list = []

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

    bill.user_id = bill_in.user_id
    bill.total_cost = total_cost
    db.commit()

    for detail in bill_details_list:
        db.refresh(detail)

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
        date=str(bill.date), 
        user_id=bill.user_id,
        cus_id= bill.cus_id,
        total_cost=total_cost,
        bill_details=response_details
    )


# DELETE /bill/{bill_id} — xóa hóa đơn
@router.delete("/bill/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    db.query(BillDetail).filter(BillDetail.bill_id == bill_id).delete()
    db.delete(bill)
    db.commit()
    return {"detail": f"Bill {bill_id} deleted successfully"}


#  GET /sales — tổng doanh thu
@router.get("/sales")
def total_sales(db: Session = Depends(get_db)):
    total = db.query(func.sum(Bill.total_cost)).scalar() or 0
    return {"total_sales": total}
