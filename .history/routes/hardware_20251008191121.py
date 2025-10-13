from fastapi import FastAPI, APIRouter, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil, os, uuid
import httpx  # để gửi dữ liệu lên web server
from websocket_manager import manager

app = FastAPI(
    title="Fruit & Hardware API",
    description="API for managing fruits, hardware, and weights",
    version="1.0.0"
)

# Cho phép ESP8266 truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Router Hardware ---
router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_image")
async def upload_image(
    file: UploadFile = File(...), 
    name: str = Form(...)
):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")

    content = await file.read()
    print(f"Received file: {file.filename}, size: {len(content)} bytes")
    print(f"Received name: {name}")
    await file.seek(0)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if os.path.exists(file_path):
        print(f"File saved successfully at: {file_path}")
    else:
        print(f"Failed to save file at: {file_path}")

    result = {
        "fruit": "",
        "confidence": None,
        "file_path": file_path,
        "name": name
    }

    await manager.broadcast({
        "type": "fruit_detected",
        "data": result
    })

    return result


@router.get("/get_weight")
async def get_weight():
    weight = 1.25 
    data = {"weight": weight}

    await manager.broadcast({
        "type": "weight",
        "data": data
    })

    return data



@router.post("/weight")
async def receive_weight_from_hardware(request: Request):
    """
    Nhận dữ liệu cân từ ESP8266 và gửi tiếp lên web thật
    """
    data = await request.json()
    weight = data.get("weight", None)
    print(f"📦 Nhận từ ESP8266: {weight} kg")

    # --- Gửi lên web server thật ---
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            resp = await client.post(WEB_SERVER_API, json={"weight": weight})
            print(f"🌐 Đẩy lên web thành công: {resp.status_code}")
        except Exception as e:
            print(f"❌ Lỗi khi đẩy lên web: {e}")

    # --- Broadcast nếu cần ---
    # await manager.broadcast({"type": "weight", "data": {"weight": weight}})

    return {"status": "ok", "received": weight}
