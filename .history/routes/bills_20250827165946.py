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
    tags= ["Bills"]
)