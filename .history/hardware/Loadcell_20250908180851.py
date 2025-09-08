import serial
import time

SERIAL_PORT = "COM3"
BAUDRATE = 9600

def get_weight_from_load_cell():
    try:
        ser = serial.Serial(SERIAL_PORT,BAUDRATE,timeout=1)
        time.sleep(2)
        ser.write(b"READ\n")
        weight = ser.readline().decode().strip()
        ser.close()
        return float(weight) if weight else None
    except Exception as e:
        return f"Lỗi : {str(e)}"
    

# debug
print("Khối lượng,",get_weight_from_load_cell(),"kg")