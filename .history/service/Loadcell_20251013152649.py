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

   
    return jsonify({"status": "ok", "received": weight}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
