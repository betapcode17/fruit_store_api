import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Bill,Fruit,BillDetail
from database import get_db
from schemas.bills import BillCreate,BillItem,BillDetailResponse,BillResponse
from schemas.bill_details import BillDetailResponse


router = APIRouter(
    tags= ["Bills"],
    prefix= "/bills"
)

# add new bill
# POST /bill
@router.post("/bill", response_model=BillResponse)
def create_bill(bill_in: BillCreate, db: Session = Depends(get_db)):
    total_cost = 0
    bill_details_list = []

    # tạo Bill
    bill = Bill(user_id=bill_in.user_id)
    db.add(bill)
    db.commit()
    db.refresh(bill)

    # xử lý từng item
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
        db.commit()
        db.refresh(detail)
        bill_details_list.append(detail)

    # cập nhật tổng tiền
    bill.total_cost = total_cost
    db.commit()
    db.refresh(bill)

    # prepare response
    response_details = []
    for d in bill_details_list:
        fruit = db.query(Fruit).filter(Fruit.id == d.fruit_id).first()
        response_details.append(BillDetailResponse(
            detail_id=d.detail_id,
            fruit_id=d.fruit_id,
            fruit_name=fruit.name,
            weight=d.weight,
            price=d.price
        ))

    return BillResponse(
        bill_id=bill.bill_id,
        date=bill.date,
        user_id=bill.user_id,
        total_cost=bill.total_cost,
        bill_details=response_details
    )
