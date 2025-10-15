from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
import urllib.request
import numpy as np
import cv2
import os
import uuid

# URL snapshot của ESP32-CAM
ESP32_URL = "http://192.168.1.21/cam-lo.jpg"

# Thư mục lưu ảnh
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Tạo router riêng
router = APIRouter(
    prefix="/ai",
    tags=["AI Capture"]
)

@router.get("/capture", summary="Chụp ảnh từ ESP32-CAM")
async def capture_image():
    """
    Lấy ảnh từ ESP32-CAM, lưu vào thư mục uploads/, 
    và trả ảnh về trình duyệt.
    """
    try:
        # --- Lấy ảnh từ ESP32-CAM ---
        img_resp = urllib.request.urlopen(ESP32_URL, timeout=5)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if frame is None:
            return JSONResponse(content={"error": "Không đọc được ảnh từ ESP32-CAM"}, status_code=400)

        # --- Lưu ảnh ---
        filename = f"{uuid.uuid4()}.jpg"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        cv2.imwrite(file_path, frame)

        print(f"📸 Ảnh đã lưu: {file_path}")

        # --- Trả ảnh về ---
        return FileResponse(file_path, media_type="image/jpeg")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
