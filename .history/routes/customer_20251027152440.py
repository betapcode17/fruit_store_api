from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from models import Customer
from schemas.customer import CustomerResponse

router = APIRouter(tags=["Customer"])

