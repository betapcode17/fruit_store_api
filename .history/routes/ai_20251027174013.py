# api_router.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import json
from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import os
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



# 🟢 GET /api/files — Trả về danh sách ảnh và JSON tương ứng
@router.get("/files", summary="Lấy danh sách ảnh và file JSON")
async def list_uploaded_files():
    try:
        files = []
        # Lặp qua từng file JSON trong thư mục
        for json_filename in os.listdir(JSON_DIR):
            if not json_filename.endswith(".json"):
                continue
            json_path = os.path.join(JSON_DIR, json_filename)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            image_name = data.get("image_name")
            image_path = os.path.join(UPLOAD_DIR, image_name) if image_name else None

            files.append({
                "json_file": json_filename,
                "json_content": data,
                "image_file": image_name,
                "image_url": f"/api/files/image/{image_name}" if image_name else None
            })

        return JSONResponse(content={"status": "success", "files": files})

    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)


# 🟡 GET /api/files/image/{filename} — Trả về file ảnh thực tế
@router.get("/files/image/{filename}", response_class=FileResponse)
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        return JSONResponse(content={"status": "error", "detail": "Image not found"}, status_code=404)
    return FileResponse(file_path)
