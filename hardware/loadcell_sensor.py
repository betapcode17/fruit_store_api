from flask import Flask
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect')
def handle_connect():
    print("🔗 ESP8266 connected!")


@socketio.on('disconnect')
def handle_disconnect():
    print("❌ ESP8266 disconnected!")


@socketio.on('weight_data')
def handle_weight(data):
    """
    ESP8266 gửi JSON dạng: {"weight": 1.25}
    """
    print(f"⚖️ Dữ liệu cân realtime: {data['weight']} kg")

    # Phát dữ liệu tới Web Client khác (nếu muốn hiển thị trên web)
    socketio.emit('new_weight', data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
