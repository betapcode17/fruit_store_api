import serial, time, os
from dotenv import load_dotenv

load_dotenv()
PORT = os.getenv("SERIAL_PORT", "COM3")
BAUD = int(os.getenv("BAUDRATE", 9600))

def read_weight_once(timeout=2.0):
    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            time.sleep(1)
            # nếu Arduino gửi liên tục, ta chỉ đọc 1 dòng
            line = ser.readline().decode().strip()
            if not line:
                return None
            try:
                return float(line)
            except:
                return line
    except Exception as e:
        return None
