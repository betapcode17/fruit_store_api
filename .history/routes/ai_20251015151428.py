# ai_router.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import requests
import uuid
import os
import json

# Tạo thư mục lưu JSON nếu chưa có
os.makedirs("received_json", exist_ok=True)

router = APIRouter(prefix="/ai", tags=["AI Capture"])

# --- POST: Nhận JSON từ đồng đội ---
@router.post("/receive", summary="Nhận JSON detections từ đồng đội AI")
async def receive_detections(data: dict):
    """
    Nhận JSON theo định dạng:
    {
        "image_name": "snapshot_004.jpg",
        "detections": [
            {"class_": "banana", "confidence": 0.94, "x1": 43.5, ...},
            ...
        ]
    }
    """
    print("📥 Received JSON:")
    print(data)

    filename = f"received_json/{uuid.uuid4()}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return JSONResponse(content={"status": "success", "saved_as": filename})


# --- GET: Test gửi JSON tới POST ---
@router.get("/test-send", summary="Test gửi JSON mẫu lên /receive")
async def test_send():
    test_json = {
        "image_name": "snapshot_004.jpg",
        "detections": [
            {"class_": "banana", "confidence": 0.94, "x1": 43.5, "y1": 82.2, "x2": 190.1, "y2": 210.6},
            {"class_": "apple", "confidence": 0.88, "x1": 220.0, "y1": 105.2, "x2": 310.3, "y2": 200.7}
        ]
    }

    # Gửi POST tới chính server này
    post_url = "http://127.0.0.1:8000/ai/receive"
    try:
        response = requests.post(post_url, json=test_json)
        return JSONResponse(content={"status": "sent", "response_from_receive": response.json()})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)
