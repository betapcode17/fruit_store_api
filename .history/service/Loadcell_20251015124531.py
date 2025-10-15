from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from routes.hardware_router import hardware_router  # Import router
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Đăng ký router (Blueprint)
app.register_blueprint(hardware_router)

current_weight = None
lock = threading.Lock()

# =====================================================
# 🚀 ESP8266 gửi dữ liệu cân
# =====================================================
@app.route('/weight', methods=['POST'])
def receive_weight():
    global current_weight
    data = request.get_json()
    weight = data.get('weight', None)

    if weight is None:
        return jsonify({"error": "Missing weight"}), 400

    with lock:
        current_weight = weight

    print("=" * 50)
    print(f"📦 Nhận từ ESP8266: {weight} kg")
    print("=" * 50)

    # ✅ Gửi realtime tới client qua WebSocket
    socketio.emit('new_weight', {'weight': weight})

    return jsonify({"status": "ok", "received": weight}), 200


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
    socketio.run(app, host='0.0.0.0', port=5000)
