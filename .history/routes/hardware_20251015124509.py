from flask import Blueprint, jsonify
from flask_socketio import emit

# Blueprint tương tự như APIRouter
hardware_router = Blueprint("hardware", __name__, url_prefix="/hardware")

# Biến toàn cục lưu cân nặng
current_weight = None

# Giả lập giá trị cân hoặc có thể cập nhật từ loadcell.py
@hardware_router.route("/get_weight", methods=["GET"])
def get_weight():
    """
    Lấy cân nặng hiện tại.
    """
    global current_weight
    if current_weight is None:
        return jsonify({"weight": None, "message": "Chưa có dữ liệu cân"})
    return jsonify({"weight": current_weight})
