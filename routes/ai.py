from fastapi import APIRouter, Depends, UploadFile, File, Form, WebSocket
from fastapi.responses import JSONResponse, FileResponse
import os, json, glob, re
from datetime import datetime
from typing import List

from fastapi.staticfiles import StaticFiles
from requests import Session

from database import get_db
from models import Fruit

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



# @router.post("/api/upload_result", summary="Nhận ảnh + JSON detections từ client")
# async def upload_result(
#     file: UploadFile = File(...),
#     data: str = Form(...)
# ):
#     try:
       
#         json_data = json.loads(data)
#         detections = json_data.get("detections", [])
#         counts = json_data.get("counts", {})

        
#         if detections:
#             main_class = max(detections, key=lambda x: x.get("confidence", 0)).get("class", "unknown")
#             count_for_class = counts.get(main_class, 0)
#         else:
#             main_class = "unknown"
#             count_for_class = 0

       
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        
#         file_ext = os.path.splitext(file.filename)[1]
#         image_filename = f"{main_class}_{count_for_class}_{timestamp}{file_ext}"
#         image_path = os.path.join(UPLOAD_DIR, image_filename)
#         with open(image_path, "wb") as f:
#             f.write(await file.read())

#         json_filename = f"{main_class}_{count_for_class}_{timestamp}.json"
#         json_path = os.path.join(JSON_DIR, json_filename)
#         with open(json_path, "w", encoding="utf-8") as f:
#             json.dump(json_data, f, ensure_ascii=False, indent=4)

       
#         final_count = sum(counts.values()) if counts else len(detections)

       
#         return JSONResponse(content={
#             "status": "success",
#             "message": "Image and JSON saved successfully",
#             "image_path": image_path,
#             "json_path": json_path,
#             "detections_count": final_count,
#             "json_content": json_data
#         })

#     except Exception as e:
#         return JSONResponse(content={
#             "status": "error",
#             "detail": str(e)
#         }, status_code=500)



def get_fruit_id_by_name_internal(name: str, db: Session):
    fruit = db.query(Fruit).filter(Fruit.name.ilike(name)).first()
    if not fruit:
        return None
    return fruit.id





# @router.post("/api/upload_result", summary="Nhận ảnh + JSON detections từ client")
# async def upload_result(
#     file: UploadFile = File(...),
#     data: str = Form(...)
# ):
#     try:
#         # Parse JSON
#         json_data = json.loads(data)
#         detections = json_data.get("detections", [])
#         counts = json_data.get("counts", {})

#         # Lấy cân nặng nếu client gửi (vd: "weight": 65.2)
#         weight = json_data.get("weight", None)

#         # Lấy class chính
#         if detections:
#             main_class = max(detections, key=lambda x: x.get("confidence", 0)).get("class", "unknown")
#             count_for_class = counts.get(main_class, 0)
#         else:
#             main_class = "unknown"
#             count_for_class = 0

#         # Tạo tên file
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         file_ext = os.path.splitext(file.filename)[1]

#         image_filename = f"{main_class}_{count_for_class}_{timestamp}{file_ext}"
#         image_path = os.path.join(UPLOAD_DIR, image_filename)
#         with open(image_path, "wb") as f:
#             f.write(await file.read())

#         # Ghi JSON (bao gồm cân nặng)
#         json_data["weight"] = weight   # 👈 Thêm cân nặng vào JSON

#         json_filename = f"{main_class}_{count_for_class}_{timestamp}.json"
#         json_path = os.path.join(JSON_DIR, json_filename)
#         with open(json_path, "w", encoding="utf-8") as f:
#             json.dump(json_data, f, ensure_ascii=False, indent=4)

#         # Tổng số đối tượng
#         final_count = sum(counts.values()) if counts else len(detections)

#         return JSONResponse(content={
#             "status": "success",
#             "message": "Image and JSON saved successfully",
#             "image_path": image_path,
#             "json_path": json_path,
#             "detections_count": final_count,
#             "weight": weight,
#             "json_content": json_data
#         })

#     except Exception as e:
#         return JSONResponse(content={
#             "status": "error",
#             "detail": str(e)
#         }, status_code=500)


@router.post("/api/upload_result", summary="Nhận ảnh + JSON detections từ client")
async def upload_result(
    file: UploadFile = File(...),
    data: str = Form(...),
    db: Session = Depends(get_db)   # 👈 THÊM DB
):
    try:
        # Parse JSON
        json_data = json.loads(data)
        detections = json_data.get("detections", [])
        counts = json_data.get("counts", {})

        # Lấy cân nặng
        weight = json_data.get("weight", None)

        # Lấy class chính
        if detections:
            main_class = max(
                detections,
                key=lambda x: x.get("confidence", 0)
            ).get("class", "unknown")
            count_for_class = counts.get(main_class, 0)
        else:
            main_class = "unknown"
            count_for_class = 0

        # 🔥 LẤY FRUIT_ID TỪ DB
        fruit_id = get_fruit_id_by_name_internal(main_class, db)

        # Tạo tên file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = os.path.splitext(file.filename)[1]

        image_filename = f"{main_class}_{count_for_class}_{timestamp}{file_ext}"
        image_path = os.path.join(UPLOAD_DIR, image_filename)
        with open(image_path, "wb") as f:
            f.write(await file.read())

        # 🔥 GHI THÊM fruit_id VÀO JSON
        json_data["weight"] = weight
        json_data["fruit_id"] = fruit_id   # 👈 THÊM Ở ĐÂY

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
            "fruit_id": fruit_id,
            "weight": weight
        })

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "detail": str(e)},
            status_code=500
        )


# async def analyze_files(base_url: str = "https://fruitstore.loca.lt"):
#     latest = None
#     latest_timestamp = ""

#     json_files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]
#     pattern = r"^(?P<class>\w+)_(?P<count>\d+)_(?P<timestamp>\d{8}_\d{6})\.json$"

#     for jf in json_files:
#         match = re.match(pattern, jf)
#         if not match:
#             continue

#         class_name = match.group("class")
#         timestamp = match.group("timestamp")

#         # ✅ Chỉ xét file mới hơn
#         if timestamp > latest_timestamp:
#             json_path = os.path.join(JSON_DIR, jf)

#             try:
#                 with open(json_path, "r", encoding="utf-8") as f:
#                     json_data = json.load(f)

#                 # 🔥 COUNT LẤY TỪ JSON
#                 count = json_data.get("counts", {}).get(class_name, 0)
#                 weight = json_data.get("weight")
#             except:
#                 continue

#             base_name = os.path.splitext(jf)[0]
#             image_files = glob.glob(os.path.join(UPLOAD_DIR, f"{base_name}.*"))
#             image_file = os.path.basename(image_files[0]) if image_files else None
#             image_url = f"{base_url}/files/image/{image_file}" if image_file else None

#             latest = {
#                 "class": class_name,
#                 "count": count,
#                 "timestamp": timestamp,
#                 "json_file": jf,
#                 "weight": weight,
#                 "image_file": image_file,
#                 "image_url": image_url
#             }

#             latest_timestamp = timestamp

#     return latest

async def analyze_files(base_url: str = "https://fruitstore.loca.lt"):
    results = {}

    json_files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]

    pattern = r"^(?P<class>\w+?)_(?P<count>\d+)_(?P<timestamp>\d{8}_\d{6})\.json$"

    for jf in json_files:
        match = re.match(pattern, jf)
        if not match:
            continue

        fruit_class = match.group("class")
        count = int(match.group("count"))
        timestamp = match.group("timestamp")

        # ❌ bỏ unknown
        if fruit_class.lower() == "unknown":
            continue

        # ✅ chỉ lấy file mới nhất cho mỗi loại quả
        if (
            fruit_class not in results
            or timestamp > results[fruit_class]["timestamp"]
        ):
            json_path = os.path.join(JSON_DIR, jf)

            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    json_data = json.load(f)

                weight = json_data.get("weight")
                fruit_id = json_data.get("fruit_id")   # 🔥 LẤY ID TỪ JSON

            except Exception:
                continue

            base_name = os.path.splitext(jf)[0]
            image_files = glob.glob(os.path.join(UPLOAD_DIR, f"{base_name}.*"))
            image_file = os.path.basename(image_files[0]) if image_files else None
            image_url = (
                f"{base_url}/files/image/{image_file}" if image_file else None
            )

            results[fruit_class] = {
                "fruit_id": fruit_id,        # ✅ ID TỪ FILE JSON
                "class": fruit_class,
                "count": count,              # ✅ từ tên file
                "timestamp": timestamp,
                "json_file": jf,
                "weight": weight,
                "image_file": image_file,
                "image_url": image_url,
            }

    return results




# ---- Broadcast update ----
async def broadcast_files_update():
    results = await analyze_files()   # ✅
    await manager.broadcast({"status": "update", "files": results})

# ---- Lấy tất cả file mới nhất ----
@router.get("/files/latest")
async def get_latest_file():
    try:
        results = await analyze_files()  # ✅
        return JSONResponse(content={"status": "success", "files": results})
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "detail": str(e)},
            status_code=500
        )


@router.delete("/files/by-fruit/{fruit_id}", summary="Xóa ảnh + JSON theo fruit_id")
async def delete_files_by_fruit_id(
    fruit_id: int,
    db: Session = Depends(get_db)
):
    # 1️⃣ Lấy fruit từ DB
    fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
    if not fruit:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "detail": "Fruit not found"}
        )

    fruit_name = fruit.name

    deleted_files = {
        "images": [],
        "jsons": []
    }

    # 2️⃣ Xóa JSON
    for jf in os.listdir(JSON_DIR):
        if jf.startswith(f"{fruit_name}_") and jf.endswith(".json"):
            path = os.path.join(JSON_DIR, jf)
            os.remove(path)
            deleted_files["jsons"].append(jf)

    # 3️⃣ Xóa ảnh
    for img in os.listdir(UPLOAD_DIR):
        if img.startswith(f"{fruit_name}_"):
            path = os.path.join(UPLOAD_DIR, img)
            os.remove(path)
            deleted_files["images"].append(img)

    # 4️⃣ Broadcast cập nhật realtime (nếu có websocket)
    await broadcast_files_update()

    return {
        "status": "success",
        "fruit_id": fruit_id,
        "fruit_name": fruit_name,
        "deleted": deleted_files
    }


@router.get("/files/latest-fruit", summary="Lấy tên quả mới nhất dựa vào tên file")
async def get_latest_fruit_name():
    latest_timestamp = ""
    latest_fruit = None
    latest_file = None

    pattern = r"^(?P<class>\w+?)_(?P<count>\d+)_(?P<timestamp>\d{8}_\d{6})\.json$"

    for jf in os.listdir(JSON_DIR):
        if not jf.endswith(".json"):
            continue

        match = re.match(pattern, jf)
        if not match:
            continue

        fruit_class = match.group("class")
        timestamp = match.group("timestamp")

        # ❌ bỏ unknown
        if fruit_class.lower() == "unknown":
            continue

        # ✅ lấy file mới nhất
        if timestamp > latest_timestamp:
            latest_timestamp = timestamp
            latest_fruit = fruit_class
            latest_file = jf

    if not latest_fruit:
        return JSONResponse(
            status_code=404,
            content={"status": "error", "detail": "No valid fruit file found"}
        )

    return {
        "status": "success",
        "fruit_name": latest_fruit,
        "json_file": latest_file,
        "timestamp": latest_timestamp
    }
