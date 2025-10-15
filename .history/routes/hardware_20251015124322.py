from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- Biến toàn cục để lưu cân nặng hiện tại ---
current_weight = None
lock = threading.Lock()  # tránh xung đột khi nhiều thiết bị gửi cùng lúc

# =====================================================
# 🚀 API REST: ESP8266 gửi dữ liệu cân qua POST
# =====================================================
@app.route('/weight', methods=['POST'])
def receive_weight():
    global current_weight
    data = request.get_json()
    weight = data.get('weight', None)

    if weight is None:
        return jsonify({"error": "Missing weight field"}), 400

    with lock:
        current_weight = weight

    print("=" * 50)
    print(f"📦 Nhận từ ESP8266: {weight} kg")
    print("=" * 50)

    # ✅ Gửi real-time tới tất cả client WebSocket
    socketio.emit('new_weight', {'weight': weight})

    return jsonify({"status": "ok", "received": weight}), 200


# =====================================================
# 📡 API REST: Client (hoặc web app) có thể GET cân hiện tại
# =====================================================
@app.route('/weight', methods=['GET'])
def get_weight():
    if current_weight is None:
        return jsonify({"weight": None, "message": "Chưa có dữ liệu cân"})
    return jsonify({"weight": current_weight})


# =====================================================
# 🔗 WebSocket events
# =====================================================
@socketio.on('connect')
def handle_connect():
    print("🔗 Web client đã kết nối!")
    emit('connected', {'message': 'WebSocket connected!'})

@socketio.on('disconnect')
def handle_disconnect():
    print("❌ Web client ngắt kết nối!")


# =====================================================
# 🏁 Chạy server Flask + WebSocket
# =====================================================
if __name__ == '__main__':
    # Chạy trên tất cả địa chỉ IP, port 5000
    socketio.run(app, host='0.0.0.0', port=5000)
