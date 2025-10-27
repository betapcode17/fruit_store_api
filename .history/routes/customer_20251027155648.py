from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from database import get_db
from models import Customer, Bill, BillDetail, Fruit
from schemas.customer import CustomerResponse
from schemas.bill import BillResponse, BillDetailResponse  # nếu bạn có file schemas/bill.py

router = APIRouter(tags=["Customer"])

# GET /viewCustomer/{cus_id}
@router.get("/viewCustomer/{cus_id}", response_model=CustomerResponse)
def view_cus(cus_id: int, db: Session = Depends(get_db)):
    # tải customer (kèm bills nếu có) để có thể tính tổng tiền an toàn
    cus = (
        db.query(Customer)
        .options(joinedload(Customer.bills))  # dùng nếu model Customer có relationship 'bills'
        .filter(Customer.cus_id == cus_id)
        .first()
    )
    if not cus:
        raise HTTPException(status_code=404, detail="customer not found")

    # Tính moneySpent: ưu tiên field trên model, nếu không có thì tổng từ bills
    money_spent = getattr(cus, "moneySpent", None)
    if money_spent is None:
        # tổng từ bills nếu quan hệ bills tồn tại
        if hasattr(cus, "bills"):
            money_spent = sum((b.total_cost or 0) for b in cus.bills)
        else:
            money_spent = 0.0

    # Trả về CustomerResponse (Pydantic sẽ map tự động nhờ orm_mode=True)
    return CustomerResponse(
        cus_id=cus.cus_id,
        name=cus.name,
        phone=getattr(cus, "phone", None),
        address=getattr(cus, "address", None),
        moneySpent=float(money_spent)
    )


# GET /ViewAllBill
# Nếu bạn muốn endpoint này, bạn cần định nghĩa BillResponse/BillDetailResponse trong schemas.
@router.get("/ViewAllBill", response_model=List[BillResponse])
def view_all_bills(db: Session = Depends(get_db)):
    bills = db.query(Bill).options(joinedload(Bill.bill_details)).all()
    all_bills = []

    for bill in bills:
        details = []
        for d in bill.bill_details:
            # lấy tên trái cây an toàn (nếu model Fruit tồn tại)
            fruit = None
            if d.fruit_id is not None:
                fruit = db.query(Fruit).filter(Fruit.id == d.fruit_id).first()
            fruit_name = fruit.name if fruit else None

            details.append(BillDetailResponse(
                detail_id=d.detail_id,
                fruit_id=d.fruit_id,
                fruit_name=fruit_name,
                weight=d.weight,
                price=d.price
            ))

        all_bills.append(BillResponse(
            bill_id=bill.bill_id,
            date=bill.date,  # nếu cần format, làm ở schema hoặc helper to_vn_time trước
            user_id=bill.user_id,
            total_cost=bill.total_cost,
            bill_details=details
        ))

    return all_bills
