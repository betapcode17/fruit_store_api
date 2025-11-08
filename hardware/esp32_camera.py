import cv2
import urllib.request
import numpy as np
import os
import base64
import json
import time
from socketio import Client
ESP32_URL = "http://192.168.1.21/cam-lo.jpg"   # URL snapshot của ESP32-CAM
SAVE_FOLDER = "uploads"
SERVER_URL = "http://localhost:5000"           # Flask server (WebSocket)
os.makedirs(SAVE_FOLDER, exist_ok=True)
sio = Client()
sio.connect(SERVER_URL)

@sio.on('response')
def on_response(data):
    """Nhận phản hồi realtime từ server"""
    print("📩 Server:", data)

count = 0
print("📡 Bắt đầu gửi ảnh từ ESP32-CAM...")

while True:
    try:
        # 1️⃣ Lấy ảnh từ ESP32-CAM
        img_resp = urllib.request.urlopen(ESP32_URL, timeout=5)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        if frame is None:
            print("⚠️ Không đọc được frame từ ESP32-CAM.")
            continue

        # 2️⃣ Lưu tạm ảnh
        filename = os.path.join(SAVE_FOLDER, f"snapshot_{count:03d}.jpg")
        cv2.imwrite(filename, frame)

        # 3️⃣ Chuyển ảnh sang base64
        _, buffer = cv2.imencode('.jpg', frame)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # 4️⃣ Gửi ảnh qua WebSocket
        sio.emit('frame', {
            "image_name": f"snapshot_{count:03d}.jpg",
            "image_data": image_base64,
            "detections": [
                {"class_": "object", "confidence": 0.9}
            ]
        })

        print(f"📤 Đã gửi: {filename}")
        count += 1

        # 5️⃣ Hiển thị ảnh tại client
        cv2.imshow("ESP32-CAM Live", frame)

    except Exception as e:
        print("❌ Lỗi khi lấy hoặc gửi ảnh:", e)

    # Thoát nếu nhấn 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # ⏱️ Gửi ảnh mỗi 3 giây (tùy chỉnh)
    time.sleep(3)

# ======================
# 🧹 Dọn dẹp
# ======================
cv2.destroyAllWindows()
sio.disconnect()
print("✅ Dừng gửi ảnh.")
