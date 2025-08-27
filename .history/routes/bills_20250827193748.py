import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Bill,Fruit,BillDetail
from database import get_db
from schemas.bills import BillCreate,BillItem,BillDetailResponse,BillResponse

router = APIRouter(
    tags= ["Bills"],
    prefix= "/bills"
)

# add new bill
@router.post("/",response_model=BillResponse)
def create_bill(bill_in: BillCreate, db: Session =  Depends(get_db)):


    total_cost = 0
    bill_detail_list =[]

    # 
    bill = Bill(user_id = bill_in.user_id)
    db.add(bill)
    db.commit()
    db.refresh(bill)

    #
    for item in bill_in.items:
        fruit = db.query(Fruit).filter(Fruit.id == item.fruit_id).first()
        if not fruit:
         raise HTTPException(status_code=404, detail=f"Fruit ID {item.fruit_id} not found")
        
        price = fruit.price * item.weight
        total_cost += price

        detail = BillDetail(
           bill_id = bill_in.bill_id,
           
        )
