from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Customer, Fruit, Bill, BillDetail, User
from schemas.statistics import RevenueDay, RevenueMonth, TopCustomer, TopFruit, RevenueFruit, TopSeller

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"]
)

# Get / revenue day
@router.get("/revenue/day", response_model=list[RevenueDay])
async def revenue_by_day(db: Session = Depends(get_db)):
    result = (
        db.query(
            func.date(Bill.date).label("day"),
            func.sum(Bill.total_cost).label("total_revenue")
        )
        .group_by(func.date(Bill.date))
        .order_by(func.date(Bill.date))
        .all()
    )
    return result


# Get / revenue month
@router.get("/revenue/month", response_model=list[RevenueMonth])
async def revenue_by_month(db: Session = Depends(get_db)):
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


# Get / top 5 fruits
@router.get("/top-fruits", response_model=list[TopFruit])
async def top_fruits(limit: int = 5, db: Session = Depends(get_db)):
    result = (
        db.query(
            Fruit.name.label("name"),
            func.sum(BillDetail.weight).label("total_weight"),
            func.sum(BillDetail.price * BillDetail.weight).label("revenue")
        )
        .join(Fruit, BillDetail.fruit_id == Fruit.id)
        .group_by(Fruit.name)
        .order_by(func.sum(BillDetail.weight).desc())
        .limit(limit)
        .all()
    )
    return result


# Get / revenue by fruits
@router.get("/revenue/by-fruits", response_model=list[RevenueFruit])
async def revenue_by_fruit(db: Session = Depends(get_db)):
    result = (
        db.query(
            Fruit.name.label("name"),
            func.sum(BillDetail.price * BillDetail.weight).label("total_revenue")
        )
        .join(Fruit, BillDetail.fruit_id == Fruit.id)
        .group_by(Fruit.name)
        .order_by(func.sum(BillDetail.price * BillDetail.weight).desc())
        .all()
    )
    return result

@router.get("/top-sellers", response_model=list[TopSeller])
async def top_sellers(limit: int = 5, db: Session = Depends(get_db)):
    result = (
        db.query(
            User.id.label("user_id"),
            User.name.label("name"),
            func.sum(Bill.total_cost).label("total_revenue")
        )
        .join(Bill, Bill.user_id == User.id)
        .group_by(User.id, User.name)
        .order_by(func.sum(Bill.total_cost).desc())
        .limit(limit)
        .all()
    )

    return result

@router.get("/top-customers", response_model=list[TopCustomer])
async def top_customers(limit: int = 5, db: Session = Depends(get_db)):
    result = (
        db.query(
            Customer.cus_id.label("cus_id"),
            Customer.name.label("name"),
            func.sum(Bill.total_cost).label("total_revenue")
        )
        .join(Bill, Bill.cus_id == Customer.cus_id)
        .group_by(Customer.cus_id, Customer.name)
        .order_by(func.sum(Bill.total_cost).desc())
        .limit(limit)
        .all()
    )

    return result