from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Customer
from schemas.customer import CustomerResponse

router = APIRouter(tags=["Customer"])


# GET /viewCustomer/{cus_id}
@router.get("/viewCustomer/{cus_id}", response_model=CustomerResponse)
def view_customer(cus_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.cus_id == cus_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer 



# GET /viewAllCustomer
@router.get("/viewAllCustomer", response_model=List[CustomerResponse])
def view_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers

# POST/customer - Thêm customer