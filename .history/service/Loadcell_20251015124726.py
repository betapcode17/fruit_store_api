from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

current_weight = None
lock = threading.Lock()

@app.route('/weight', methods=['POST'])
def receive_weight():
    """
    Nhận dữ liệu từ ESP8266 (POST JSON: {"weight": 2.5})
    """
    global current_weight
    data = request.get_json()
    weight = data.get('weight')

    if weight is None:
        return jsonify({"error": "Missing weight"}), 400

    with lock:
        current_weight = weight

    print("=" * 40)
    print(f"📦 Nhận từ ESP8266: {weight} kg")
    print("=" * 40)

    # Gửi dữ liệu realtime đến WebSocket client (nếu có)
    socketio.emit('new_weight', {'weight': weight})

    return jsonify({"status": "ok", "received": weight}), 200


@app.route('/weight', methods=['GET'])
def get_weight():
    """
    Cho phép FastAPI hoặc Web lấy cân hiện tại
    """
    if current_weight is None:
        return jsonify({"weight": None, "message": "Chưa có dữ liệu cân"})
    return jsonify({"weight": current_weight})


@socketio.on('connect')
def on_connect():
    print("🔗 Web client đã kết nối!")
    emit('connected', {'message': 'WebSocket connected!'})

@socketio.on('disconnect')
def on_disconnect():
    print("❌ Web client ngắt kết nối!")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
