from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import Customer
from schemas.customer import CustomerResponse

router = APIRouter(tags=["Customer"])

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