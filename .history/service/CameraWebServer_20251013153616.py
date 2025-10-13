import cv2
import urllib.request
import numpy as np
import time
import os

# URL snapshot của ESP32-CAM 
url = "http://192.168.1.22/cam-lo.jpg"

# Thư mục lưu ảnh
save_folder = "snapshots"
os.makedirs(save_folder, exist_ok=True)  # tạo folder nếu chưa có

count = 0
while True:
    try:
        # Lấy ảnh từ ESP32-CAM
        img_resp = urllib.request.urlopen(url)
        img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        
        if frame is not None:
            # Lưu ảnh
            filename = os.path.join(save_folder, f"snapshot_{count:03d}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Đã lưu: {filename}")

            # Hiển thị ảnh
            cv2.imshow("ESP32 Snapshot", frame)
            count += 1
        else:
            print("Không đọc được frame")

    except Exception as e:
        print("Lỗi:", e)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Đợi 5 giây trước khi chụp ảnh tiếp theo
    time.sleep(5)

cv2.destroyAllWindows()