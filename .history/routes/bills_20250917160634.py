from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import Bill, BillDetail, Fruit
from schemas.bills import BillCreate, BillResponse
from schemas.bill_details import BillDetailResponse
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

# POST /bill
@router.post("/bill", response_model=BillResponse)
def create_bill(bill_in: BillCreate, db: Session = Depends(get_db)):
    total_cost = 0
    bill_details_list = []

    bill = Bill(user_id=bill_in.user_id, date=datetime.utcnow())
    db.add(bill)
    db.commit()
    db.refresh(bill)

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
        ) for d in bill_details_list
    ]

    return BillResponse(
        bill_id=bill.bill_id,
        date=to_vn_time(bill.date),
        user_id=bill.user_id,
        total_cost=total_cost,
        bill_details=response_details
    )

# GET /viewBill/{bill_id}
@router.get("/viewBill/{bill_id}", response_model=BillResponse)
def view_bill(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    response_details = [
        BillDetailResponse(
            detail_id=d.detail_id,
            fruit_id=d.fruit_id,
            fruit_name=db.query(Fruit).filter(Fruit.id == d.fruit_id).first().name,
            weight=d.weight,
            price=d.price
        ) for d in bill.bill_details
    ]

    return BillResponse(
        bill_id=bill.bill_id,
        date=to_vn_time(bill.date),
        user_id=bill.user_id,
        total_cost=bill.total_cost,
        bill_details=response_details
    )

# GET /ViewAllBill
@router.get("/ViewAllBill", response_model=List[BillResponse])
def view_all_bills(db: Session = Depends(get_db)):
    bills = db.query(Bill).all()
    all_bills = []

    for bill in bills:
        details = [
            BillDetailResponse(
                detail_id=d.detail_id,
                fruit_id=d.fruit_id,
                fruit_name=db.query(Fruit).filter(Fruit.id == d.fruit_id).first().name,
                weight=d.weight,
                price=d.price
            ) for d in bill.bill_details
        ]
        all_bills.append(BillResponse(
            bill_id=bill.bill_id,
            date=to_vn_time(bill.date),
            user_id=bill.user_id,
            total_cost=bill.total_cost,
            bill_details=details
        ))

    return all_bills

# GET /sales
@router.get("/sales")
def total_sales(db: Session = Depends(get_db)):
    total = db.query(func.sum(Bill.total_cost)).scalar() or 0
    return {"total_sales": total}
