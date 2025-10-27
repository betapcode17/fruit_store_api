from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import Customer
from schemas.customer import CustomerResponse

router = APIRouter(tags=["Customer"])

# GET /viewCustomer/{cus_id}
@router.get("/viewCustomer/{cus_id}", response_model=CustomerResponse)
def view_cus(cus_id: int, db: Session = Depends(get_db)):
    cus = db.query(Customer).filter(Customer.cus_id == cus_id).first()
    if not cus:
        raise HTTPException(status_code=404, detail="cus not found")

    response_details = [
        CustomerResponse(
            cus_id=d.cus_id,
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