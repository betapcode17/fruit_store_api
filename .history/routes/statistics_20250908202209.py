from fastapi import APIRouter,Depends,HTTPException

router = APIRouter(
    prefix="/statistics"
    tags=["Statistics"]
)

# Get/
@router.get("/revenue/day")
def revenue_by_day(db: Session = Depends(get_db)):