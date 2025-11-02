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





# 🟢 GET /api/files/latest — Lấy JSON & ảnh mới nhất
@router.get("/files/latest", summary="Lấy file JSON và ảnh mới nhất")
async def get_latest_file():
    try:
        json_files = [
            os.path.join(JSON_DIR, f)
            for f in os.listdir(JSON_DIR)
            if f.endswith(".json")
        ]

        if not json_files:
            return JSONResponse(content={"status": "error", "detail": "No JSON files found"}, status_code=404)

        # 🔹 Lấy file mới nhất theo thời gian sửa đổi
        latest_json = max(json_files, key=os.path.getmtime)

        with open(latest_json, "r", encoding="utf-8") as f:
            data = json.load(f)

        image_name = data.get("image_name")
        image_path = os.path.join(UPLOAD_DIR, image_name) if image_name else None

        response = {
            "status": "success",
            "latest_json_file": os.path.basename(latest_json),
            "json_content": data,
            "image_file": image_name,
            "image_url": f"/api/files/image/{image_name}" if image_name else None
        }

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
