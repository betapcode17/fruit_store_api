from pydantic import BaseModel
from typing import Optional
from datetime import date

class BillCreate(BaseModel):
    date : date
    total_cost : float