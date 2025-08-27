import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Bill
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
    bill = Bill(**bill_in.dict())
    db.add(bill)
    db.commit()
    db.refresh(bill)

    #
    for item in bill_in.items
