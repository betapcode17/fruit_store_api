# ai_router.py
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
import os
import uuid

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

router = APIRouter(prefix="/ai", tags=["AI Upload"])

@router.post("/upload", summary="Upload ảnh và lưu vào uploads")
async def upload_image(file: UploadFile = File(...)):
    # Tạo tên file duy nhất
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Lưu file
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    return JSONResponse(content={"status": "success", "saved_as": filepath})
