from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/weight', methods=['POST'])
def receive_weight():
    data = request.get_json()
    weight = data.get('weight', None)

    # ✅ In rõ ràng ra terminal
    print("=" * 50)
    print(f"📦  Nhận từ ESP8266: {weight} kg")
    print("=" * 50)

    # ✅ (Không gửi lên server, chỉ phản hồi ESP)
    return jsonify({"status": "ok", "received": weight}), 200


if __name__ == '__main__':
    # host=0.0.0.0 để ESP8266 trong mạng LAN có thể truy cập Flask
    app.run(host='0.0.0.0', port=5000)
