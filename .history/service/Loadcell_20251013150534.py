import time
import threading
from flask import Flask
from flask_socketio import SocketIO, emit
import socketio

# ========================
# 🚀 PHẦN SERVER
# ========================
app = Flask(__name__)
socketio_server = SocketIO(app, cors_allowed_origins="*")

@socketio_server.on('connect')
def handle_connect():
    print("🔗 Client đã kết nối WebSocket")

@socketio_server.on('send_weight')
def handle_weight(data):
    weight = data.get('weight')
    print(f"📦 Nhận từ client: {weight} kg")

def run_server():
    socketio_server.run(app, host='0.0.0.0', port=5000)

# ========================
# 💻 PHẦN CLIENT (gửi dữ liệu liên tục)
# ========================
def run_client():
    time.sleep(2)  # Đợi server khởi động
    sio = socketio.Client()
    sio.connect('http://localhost:5000')

    try:
        weight = 1.0
        while True:
            sio.emit('send_weight', {'weight': weight})
            print(f"📤 Gửi: {weight} kg")
            weight += 0.5
            time.sleep(1)
    except KeyboardInterrupt:
        sio.disconnect()
        print("❌ Client ngắt kết nối")

# ========================
# 🎯 CHẠY CẢ HAI
# ========================
if __name__ == '__main__':
    threading.Thread(target=run_server, daemon=True).start()
    run_client()
