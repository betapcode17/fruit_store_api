from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Customer
from schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)



# GET /viewCustomer/{cus_id}
@router.get("/{cus_id}", response_model=CustomerResponse)
def view_customer(cus_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.cus_id == cus_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer 



# GET /viewAllCustomer
@router.get("/", response_model=List[CustomerResponse])
def view_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers

# POST/customer - Thêm customer
@router.post("/",response_model=CustomerResponse)
def create_customer(cus_in : CustomerCreate, db: Session =  Depends(get_db)):
    customer = Customer(**cus_in.dict())
    db.add(customer)
    db.commit(customer)
    db.refresh(customer)
    return customer

# UPDATE/customer 
@router.put("/{cus_id}",response_model=CustomerResponse)
def update_cus(cus_id: int, cus_in: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.cus_id == cus_id).first()
    if not customer :
        raise HTTPException(status_code=404, detail="customer not found")
    for key, value in cus_in.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer

# search fruit by keyword
@router.get("/search", response_model=list[CustomerResponse])
def search_fruit(keyword: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(
        or_(
            Fruit.name.ilike(f"%{keyword}%"),
            Fruit.description.ilike(f"%{keyword}%")
        )
    ).all()
    if not fruits:
        raise HTTPException(status_code=404, detail="No fruits found")
    return fruits