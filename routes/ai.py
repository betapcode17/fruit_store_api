from fastapi import APIRouter, UploadFile, File, Form, WebSocket
from fastapi.responses import JSONResponse, FileResponse
import os, json, glob, re
from datetime import datetime
from typing import List

from fastapi.staticfiles import StaticFiles

# ===== Router =====
router = APIRouter(tags=["AI Upload"])


router = APIRouter(tags=["AI Upload"])

# ---- Thư mục lưu trữ ----
UPLOAD_DIR = "uploads"
JSON_DIR = "json_results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# ---- Mount thư mục uploads để trả ảnh trực tiếp ----
# Đường dẫn URL sẽ là /files/image/<filename>
router.mount("/files/image", StaticFiles(directory=UPLOAD_DIR), name="files")

# ---- WebSocket manager ----
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

# ---- WebSocket endpoint ----
@router.websocket("/ws/files")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket)



@router.post("/api/upload_result", summary="Nhận ảnh + JSON detections từ client")
async def upload_result(
    file: UploadFile = File(...),
    data: str = Form(...)
):
    try:
       
        json_data = json.loads(data)
        detections = json_data.get("detections", [])
        counts = json_data.get("counts", {})

        
        if detections:
            main_class = max(detections, key=lambda x: x.get("confidence", 0)).get("class", "unknown")
            count_for_class = counts.get(main_class, 0)
        else:
            main_class = "unknown"
            count_for_class = 0

       
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        
        file_ext = os.path.splitext(file.filename)[1]
        image_filename = f"{main_class}_{count_for_class}_{timestamp}{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as f:
            f.write(await file.read())

        json_filename = f"{main_class}_{count_for_class}_{timestamp}.json"
        json_path = os.path.join(JSON_DIR, json_filename)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

       
        final_count = sum(counts.values()) if counts else len(detections)

       
        return JSONResponse(content={
            "status": "success",
            "message": "Image and JSON saved successfully",
            "image_path": image_path,
            "json_path": json_path,
            "detections_count": final_count,
            "json_content": json_data
        })

    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "detail": str(e)
        }, status_code=500)






# ---- Phân tích file JSON + ảnh ----
def analyze_files(base_url: str = "https://yoursubdomain.loca.lt"):
    results = {}
    json_files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]

    # Regex: Class_Count_YYYYMMDD_HHMMSS.json
    pattern = r"^(?P<class>\w+)_(?P<count>\d+)_(?P<timestamp>\d{8}_\d{6})\.json$"

    for jf in json_files:
        match = re.match(pattern, jf)
        if not match:
            continue

        class_name = match.group("class")
        count = int(match.group("count"))
        timestamp = match.group("timestamp")

        # Nếu class đã tồn tại, cập nhật count/timestamp nếu khác
        if class_name in results:
            if results[class_name]["count"] != count:
                results[class_name]["count"] = count
                results[class_name]["timestamp"] = timestamp
        else:
            results[class_name] = {
                "count": count,
                "timestamp": timestamp,
                "json_file": jf
            }

        # ---- Lấy ảnh tương ứng ----
        base_name = os.path.splitext(jf)[0]
        image_files = glob.glob(os.path.join(UPLOAD_DIR, f"{base_name}.*"))
        image_file = os.path.basename(image_files[0]) if image_files else None

        # ---- Tạo URL ảnh ----
        image_url = f"{base_url}/files/image/{image_file}" if image_file else None

        results[class_name]["image_file"] = image_file
        results[class_name]["image_url"] = image_url

    # 🔥 Bỏ qua các class "unknown"
    results = {k: v for k, v in results.items() if k.lower() != "unknown"}

    return results



# ---- Broadcast update ----
async def broadcast_files_update():
    results = analyze_files()
    await manager.broadcast({"status": "update", "files": results})

# ---- Lấy tất cả file mới nhất ----
@router.get("/files/latest")
async def get_latest_file():
    try:
        results = analyze_files()
        return JSONResponse(content={"status": "success", "files": results})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
