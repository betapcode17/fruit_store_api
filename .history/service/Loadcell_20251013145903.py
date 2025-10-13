from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Cho phép mọi client kết nối

# Khi client kết nối
@socketio.on('connect')
def handle_connect():
    print("🔗 Client đã kết nối WebSocket")
    emit('connected', {'message': 'Kết nối thành công!'})

# Khi client gửi dữ liệu (ví dụ: trọng lượng)
@socketio.on('send_weight')
def handle_weight(data):
    weight = data.get('weight')
    print(f"📦 Nhận từ client: {weight} kg")

    # (Tuỳ chọn) Gửi lại phản hồi
    emit('server_response', {'message': f'Đã nhận {weight} kg'})

# Khi client ngắt kết nối
@socketio.on('disconnect')
def handle_disconnect():
    print("❌ Client đã ngắt kết nối")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
import socketio

sio = socketio.Client()

@sio.on('connected')
def on_connect(data):
    print("✅ Server:", data)

@sio.on('server_response')
def on_response(data):
    print("📨 Phản hồi từ server:", data)

sio.connect('http://localhost:5000')
sio.emit('send_weight', {'weight': 2.5})
