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


# api_router.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import json

router = APIRouter(prefix="/api", tags=["AI Upload"])

# Tạo thư mục lưu trữ nếu chưa có
UPLOAD_DIR = "uploads"
JSON_DIR = "json_results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)


@router.post("/upload_result", summary="Nhận ảnh + JSON detections từ client")
async def upload_result(
    file: UploadFile = File(...),
    data: str = Form(...)
):
    """
    Client gửi form-data:
    - file: ảnh (jpg, png, ...)
    - data: JSON dạng text, ví dụ:
        {
            "image_id": "snapshot_001",
            "image_name": "snapshot_001.jpg",
            "detections": [
                {"class_": "banana", "confidence": 0.94, "x1": 12, "y1": 34, "x2": 56, "y2": 78}
            ]
        }
    """
    try:
        # ---- 1️⃣ Lưu ảnh ----
        file_ext = os.path.splitext(file.filename)[1]
        image_filename = f"{uuid.uuid4()}{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as f:
            f.write(await file.read())

        # ---- 2️⃣ Lưu JSON ----
        json_data = json.loads(data)  # parse chuỗi JSON
        json_filename = f"{uuid.uuid4()}.json"
        json_path = os.path.join(JSON_DIR, json_filename)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        # ---- 3️⃣ Trả về thông tin ----
        return JSONResponse(content={
            "status": "success",
            "message": "Image and JSON saved successfully",
            "image_path": image_path,
            "json_path": json_path,
            "json_content": json_data
        })

    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "detail": str(e)
        }, status_code=500)

