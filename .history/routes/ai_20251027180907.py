# api_router.py
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
import os
import uuid
import json
import os
import glob
from fastapi.responses import FileResponse


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



@router.get("/files/latest", summary="Lấy file JSON và ảnh mới nhất")
async def get_latest_file():
    try:
        # 🟡 1. Lấy danh sách file JSON
        json_files = [
            os.path.join(JSON_DIR, f)
            for f in os.listdir(JSON_DIR)
            if f.endswith(".json")
        ]

        # 🟡 2. Lấy file JSON mới nhất (nếu có)
        latest_json = max(json_files, key=os.path.getmtime) if json_files else None
        json_data = None
        if latest_json:
            with open(latest_json, "r", encoding="utf-8") as f:
                json_data = json.load(f)

        # 🟢 3. Lấy file ảnh mới nhất trong thư mục uploads
        image_files = glob.glob(os.path.join(UPLOAD_DIR, "*.png")) + \
                      glob.glob(os.path.join(UPLOAD_DIR, "*.jpg")) + \
                      glob.glob(os.path.join(UPLOAD_DIR, "*.jpeg"))

        latest_image = max(image_files, key=os.path.getmtime) if image_files else None

        # 🟣 4. Chuẩn bị phản hồi
        response = {
            "status": "success",
            "latest_json_file": os.path.basename(latest_json) if latest_json else None,
            "json_content": json_data,
            "latest_image_file": os.path.basename(latest_image) if latest_image else None,
            "latest_image_url": f"/api/files/image/{os.path.basename(latest_image)}" if latest_image else None
        }

        # 🧩 Nếu không có file nào thì báo lỗi
        if not latest_json and not latest_image:
            return JSONResponse(content={"status": "error", "detail": "No files found"}, status_code=404)

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
    

@router.get("/files/image/{filename}", summary="Trả về ảnh theo tên file")
async def get_image(filename: str):
    image_path = os.path.join(UPLOAD_DIR, filename)

    # 🟡 Kiểm tra file tồn tại
    if not os.path.exists(image_path):
        return JSONResponse(content={"status": "error", "detail": "Image not found"}, status_code=404)

    # 🟢 Trả ảnh về client
    return FileResponse(image_path, media_type="image/jpeg")