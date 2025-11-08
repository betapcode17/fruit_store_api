# ws_router.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import os, json, uuid, base64

router = APIRouter(prefix="/ws", tags=["WebSocket AI Upload"])

UPLOAD_DIR = "uploads"
JSON_DIR = "json_results"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)


@router.websocket("/upload")
async def websocket_upload(websocket: WebSocket):
    await websocket.accept()
    print("📡 Client connected")

    last_json_signature = None  # 🔹 lưu dấu vết json trước

    try:
        while True:
            data = await websocket.receive_json()

            image_name = data.get("image_name", f"{uuid.uuid4()}.jpg")
            image_base64 = data.get("image_data")
            detections = data.get("detections", [])

            if not image_base64:
                await websocket.send_json({"status": "error", "detail": "No image data"})
                continue

            # 1️⃣ Tính "dấu vết" (signature) cho JSON để phát hiện trùng
            json_signature = json.dumps(detections, sort_keys=True)

            # 🔸 Nếu trùng với frame trước → bỏ qua
            if json_signature == last_json_signature:
                continue

            # Cập nhật lại bản mới
            last_json_signature = json_signature

            # 2️⃣ Giải mã ảnh và lưu
            image_bytes = base64.b64decode(image_base64)
            image_path = os.path.join(UPLOAD_DIR, image_name)
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # 3️⃣ Lưu JSON detections
            json_filename = f"{uuid.uuid4()}.json"
            json_path = os.path.join(JSON_DIR, json_filename)
            json_data = {
                "image_name": image_name,
                "detections": detections,
                "count": len(detections)
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

            # 4️⃣ Gửi phản hồi realtime
            await websocket.send_json({
                "status": "success",
                "message": "New frame detected",
                "image_saved": image_name,
                "detections_count": len(detections),
                "detections": detections
            })

    except WebSocketDisconnect:
        print("❌ Client disconnected")
    except Exception as e:
        await websocket.send_json({"status": "error", "detail": str(e)})
