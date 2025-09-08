from fastapi import APIRouter,HTTPException

router = APIRouter(
    tags=["Hard Ware"]
)

# get Weight
@router.get("/getWeight")
def get_weight():
    weight = get_weight()

# get image