from fastapi import APIRouter
from fastapi.responses import JSONResponse
import httpx

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"]
)

# URL Flask server
LOADCELL_URL = "http://localhost:5000/weight"

@router.get("/get_weight")
async def get_weight_from_flask():
    """
    Gọi sang Flask server để lấy dữ liệu cân realtime.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(LOADCELL_URL)
            response.raise_for_status()
            data = response.json()
        print(f"📡 FastAPI nhận dữ liệu cân: {data}")
        return JSONResponse(content=data)
    except httpx.HTTPStatusError as e:
        print(f"❌ HTTP error: {e.response.status_code}")
        return JSONResponse(content={"error": f"HTTP error {e.response.status_code}"}, status_code=e.response.status_code)
    except Exception as e:
        print(f"❌ Lỗi khi lấy dữ liệu cân từ Flask: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
