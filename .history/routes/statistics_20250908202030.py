from fastapi import APIRouter

router = APIRouter(
    prefix="/statistics"
    tags=["Statistics"]
)

# Get/
@router.get("")