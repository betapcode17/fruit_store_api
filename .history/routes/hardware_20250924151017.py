from fastapi import APIRouter, UploadFile, File, Form
import shutil, os, uuid
from websocket_manager import manager
from fastapi import APIRouter
from websocket_manager import manager
import hx711  # type: ignore # hoặc thư viện Load Cell bạn dùng
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

    # Kết quả trả về, fruit và confidence để trống tạm
    result = {
        "fruit": "",          # Chưa xác định, có thể cập nhật sau
        "confidence": None,   # Chưa xác định
        "file_path": file_path,
        "name": name
    }

    await manager.broadcast({
        "type": "fruit_detected",
        "data": result
    })

    return result

# Khởi tạo cân HX711 (chỉnh chân GPIO và tỉ lệ calibrate)
hx = hx711.HX711(dout_pin=5, pd_sck_pin=6)
hx.set_scale_ratio(2280)
hx.reset()
hx.tare()

@router.get("/get_weight")
async def get_weight():
    # Lấy trọng lượng thực từ Load Cell
    weight = hx.get_weight_mean(5)  # trung bình 5 lần đọc
    data = {"weight": weight}

    # Gửi broadcast tới WebSocket client
    await manager.broadcast({
        "type": "weight",
        "data": data
    })

    return data