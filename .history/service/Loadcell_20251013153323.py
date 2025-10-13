from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- API REST: vẫn giữ để ESP8266 gửi dữ liệu bằng POST nếu cần ---
@app.route('/weight', methods=['POST'])
def receive_weight():
    data = request.get_json()
    weight = data.get('weight', None)

    print("=" * 50)
    print(f"📦 Nhận từ ESP8266: {weight} kg")
    print("=" * 50)

    # ✅ Phát dữ liệu ra tất cả client WebSocket đang kết nối
    socketio.emit('new_weight', {'weight': weight})

    return jsonify({"status": "ok", "received": weight}), 200

# --- WebSocket: khi client kết nối ---
@socketio.on('connect')
def handle_connect():
    print("🔗 Web client đã kết nối!")
    emit('connected', {'message': 'WebSocket connected!'})

# --- Khi client ngắt kết nối ---
@socketio.on('disconnect')
def handle_disconnect():
    print("❌ Web client ngắt kết nối!")


if __name__ == '__main__':
    # Dùng eventlet để hỗ trợ WebSocket
    socketio.run(app, host='0.0.0.0', port=5000)
