from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép kết nối từ ESP8266

# --- API REST nhận dữ liệu từ ESP8266 ---
@app.route('/weight', methods=['POST'])
def receive_weight():
    data = request.get_json()
    weight = data.get('weight', None)

    print(f"📦 Nhận từ ESP8266: {weight} kg")

    # ✅ Phát dữ liệu cho tất cả client WebSocket đang kết nối
    socketio.emit('new_weight', {'weight': weight})
    return jsonify({"status": "ok", "received": weight}), 200


# --- WebSocket event: Khi client (web/app) kết nối ---
@socketio.on('connect')
def handle_connect():
    print("🔗 Client đã kết nối qua WebSocket")
    emit('connected', {'message': 'WebSocket connected!'})

# --- WebSocket event: Khi client ngắt kết nối ---
@socketio.on('disconnect')
def handle_disconnect():
    print("❌ Client đã ngắt kết nối")


if __name__ == '__main__':
    # Dùng eventlet để hỗ trợ WebSocket real-time
    socketio.run(app, host='0.0.0.0', port=5000)
