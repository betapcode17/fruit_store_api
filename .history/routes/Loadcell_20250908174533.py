from fastapi import APIRouter,HTTPException

router = APIRouter(
    tags=["Load Cell"]
)

# get Weight
@router.get("/getWeight")
def get_weight():
    