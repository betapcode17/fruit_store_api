from fastapi import APIRouter, UploadFile, File, Form
import shutil, os, uuid
from websocket_manager import manager

router = APIRouter(
    prefix="/hardware",
    tags=["Hardware"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload_image")
async def upload_image(
    file: UploadFile = File(...), 
    name: str = Form(...)
):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.jpg")

    content = await file.read()
    print(f"Received file: {file.filename}, size: {len(content)} bytes")
    print(f"Received name: {name}")
    await file.seek(0)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if os.path.exists(file_path):
        print(f"File saved successfully at: {file_path}")
    else:
        print(f"Failed to save file at: {file_path}")

    # Kết quả trả về, fruit và confidence để trống tạm
    result = {
        "fruit": "",          # Chưa xác định, có thể cập nhật sau
        "confidence": None,   # Chưa xác định
        "file_path": file_path,
        "name": name
    }

    await manager.broadcast({
        "type": "fruit_detected",
        "data": result
    })

    return result


@router.get("/get_weight")
async def get_weight():
    weight = 1.25 
    data = {"weight": weight}

    await manager.broadcast({
        "type": "weight",
        "data": data
    })

    return data



from flask import Flask, request, jsonify
import requests  # dùng để gửi dữ liệu tiếp lên web thật

app = Flask(__name__)

# Địa chỉ web thật của bạn (API endpoint trên server)
WEB_SERVER_API = "https://yourweb.com/api/weight"

@app.route('/weight', methods=['POST'])
def receive_weight():
    data = request.get_json()
    weight = data.get('weight', None)

    print(f"📦 Nhận từ ESP8266: {weight} kg")

    # ✅ Gửi tiếp dữ liệu lên web server thật
    try:
        response = requests.post(WEB_SERVER_API, json={"weight": weight}, timeout=5)
        print(f"🌐 Đẩy lên web thành công: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi đẩy lên web: {e}")

    return jsonify({"status": "ok", "received": weight}), 200


if __name__ == '__main__':
    # host=0.0.0.0 để ESP8266 trong mạng LAN có thể truy cập Flask
    app.run(host='0.0.0.0', port=5000)
