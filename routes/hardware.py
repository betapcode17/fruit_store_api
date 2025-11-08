from fastapi import APIRouter
from fastapi.responses import JSONResponse
import httpx

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"]
)

LOADCELL_URL = "http://localhost:5000/weight"  # Flask endpoint

@router.get("/get_weight")
async def get_weight_from_flask():
    """
    Gọi sang Flask để lấy dữ liệu cân nặng mới nhất.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(LOADCELL_URL)
            data = response.json()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


