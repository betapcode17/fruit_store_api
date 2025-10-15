from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# === Cấu hình đường dẫn lưu ảnh tạm ===
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === API: Nhận ảnh từ ESP32 hoặc Web Client ===
@app.route('/ai/recognize', methods=['POST'])
def recognize_fruit():
    if 'image' not in request.files:
        return jsonify({"error": "Thiếu file ảnh"}), 400

    image_file = request.files['image']
    file_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(file_path)

    # --- Gọi AI model (ví dụ gọi sang server AI thật) ---
    # Ở đây demo giả lập: bạn thay bằng model thật sau
    # Ví dụ: gọi tới FastAPI hoặc Flask khác xử lý AI
    # response = requests.post("http://localhost:8000/predict", files={"file": open(file_path, "rb")})
    # result = response.json()

    # Giả lập kết quả AI trả về
    fake_result = {
        "fruit_id": "F001",
        "fruit_name": "Banana",
        "confidence": 0.98,
        "image_url": f"/{file_path}"
    }

    print("📸 Ảnh nhận từ client:", image_file.filename)
    print("🔍 Kết quả AI:", fake_result)

    return jsonify(fake_result), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
