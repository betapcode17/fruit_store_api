from fastapi import APIRouter

router = APIRouter(
    prefix="/statistics"
    tags=["Statistics"]
)

# Get/
@router.get("/revenue/day")
def revenue_by_day():