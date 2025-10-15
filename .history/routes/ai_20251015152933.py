# api_router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
import uuid
import json

router = APIRouter(prefix="/api", tags=["AI Upload"])

# Thư mục lưu JSON
JSON_DIR = "json_results"
os.makedirs(JSON_DIR, exist_ok=True)

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
    # Tạo file JSON duy nhất
    filename = f"{uuid.uuid4()}.json"
    filepath = os.path.join(JSON_DIR, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return JSONResponse(content={"status": "success", "saved_as": filepath})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
