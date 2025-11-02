# api_router.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import json

router = APIRouter(prefix="/api", tags=["AI Upload"])

# Thư mục lưu ảnh và JSON
UPLOAD_DIR = "uploads"
JSON_DIR = "json_results"

# Tạo thư mục nếu chưa tồn tại
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

@router.post("/upload_image", summary="Upload ảnh từ client")
async def upload_image(file: UploadFile = File(...)):
    """
    API này dùng để upload ảnh từ client.
    Ảnh được lưu trong thư mục 'uploads/'.
    """
    try:
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        # Lưu file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return JSONResponse(content={
            "status": "success",
            "message": "File uploaded successfully",
            "filename": new_filename,
            "path": file_path
        })
    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "detail": str(e)
        }, status_code=500)


@router.post("/upload_result", summary="Nhận JSON detections từ client Python")
async def upload_result(data: dict):
    """
    Nhận JSON theo định dạng:
    {
        "image_id": "snapshot_001",
        "image_name": "snapshot_001.jpg",
        "detections": [
            {"class_": "banana", "confidence": 0.94, "x1": ..., "y1": ..., "x2": ..., "y2": ...},
            ...
        ]
    }
    """
    filename = f"{uuid.uuid4()}.json"
    filepath = os.path.join(JSON_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return JSONResponse(content={"status": "success", "saved_as": filepath})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
