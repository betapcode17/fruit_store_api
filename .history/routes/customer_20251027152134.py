from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import Bill, BillDetail, Fruit
from schemas.bills import BillCreate, BillResponse
from schemas.bill_details import BillDetailResponse
from datetime import datetime
import pytz