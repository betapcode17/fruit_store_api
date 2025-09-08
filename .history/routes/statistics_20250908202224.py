from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import Fruit
from database import get_db
router = APIRouter(
    prefix="/statistics"
    tags=["Statistics"]
)

# Get/
@router.get("/revenue/day")
def revenue_by_day(db: Session = Depends(get_db)):
    