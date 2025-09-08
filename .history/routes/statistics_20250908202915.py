from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Fruit
from database import get_db
from models import Bill,BillDetail
router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)

# Get/day
@router.get("/revenue/day")
def revenue_by_day(db: Session = Depends(get_db)):
    result =(db.query(func.date(Bill.date).label("day"),
             func.sum(Bill.total_cost).label("total_revenue"))).group_by(func.date(Bill.date)).order_by(func.date(Bill.date)).all()
    return result

# Get/ month
@router.get("/revenue/month")
def revenue_by_month(db : Session = Depends(get_db)):
    result = (
        db.query(
            func.extract("year", Bill.date).label("year"),
            func.extract("month", Bill.date).label("month"),
            func.sum(Bill.total_cost).label("total_revenue")
        )
        .group_by(func.extract("year", Bill.date), func.extract("month", Bill.date))
        .order_by("year", "month")
        .all()
    )
    return result