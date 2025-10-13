import time
import threading
from flask import Flask
from flask_socketio import SocketIO, emit
import socketio

# ========================
# 🚀 PHẦN SERVER (Flask)
# ========================
app = Flask(__name__)
socketio_server = SocketIO(app, cors_allowed_origins="*")

@socketio_server.on('connect')
def handle_connect():
    print("🔗 Client đã kết nối WebSocket")
    emit('connected', {'message': 'Kết nối thành công!'})

@socketio_server.on('send_weight')
def handle_weight(data):
    weight = data.get('weight')
    print(f"📦 Nhận từ client: {weight} kg")
    emit('server_response', {'message': f'Đã nhận {weight} kg'})

@socketio_server.on('disconnect')
def handle_disconnect():
    print("❌ Client đã ngắt kết nối")

def run_server():
    socketio_server.run(app, host='0.0.0.0', port=5000)

# ========================
# 💻 PHẦN CLIENT (Socket.IO)
# ========================
def run_client():
    time.sleep(2)  # Đợi server khởi động
    sio = socketio.Client()

    @sio.on('connected')
    def on_connect(data):
        print("✅ Server:", data)

    @sio.on('server_response')
    def on_response(data):
        print("📨 Phản hồi từ server:", data)

    sio.connect('http://localhost:5000')
    sio.emit('send_weight', {'weight': 2.5})
    time.sleep(2)
    sio.disconnect()

# ========================
# 🎯 CHẠY CẢ HAI
# ========================
if __name__ == '__main__':
    # Chạy server trong thread riêng
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # Chạy client test
    run_client()
