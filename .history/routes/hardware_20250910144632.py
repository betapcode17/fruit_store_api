from fastapi import APIRouter, UploadFile, File, Depends
import shutil, os, uuid
from websocket_manager import manager

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")

    # Log thông tin file
    content = await file.read()
    print(f"Received file: {file.filename}, size: {len(content)} bytes")
    await file.seek(0)  # Reset con trỏ file về đầu

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Kiểm tra file có được lưu không
    if os.path.exists(file_path):
        print(f"File saved successfully at: {file_path}")
    else:
        print(f"Failed to save file at: {file_path}")

    fruit = "Banana"
    confidence = 0.92
    result = {
        "fruit": fruit,
        "confidence": confidence,
        "file_path": file_path
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
