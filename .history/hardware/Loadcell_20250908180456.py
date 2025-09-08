import serial
import time

SERIAL_PORT = "COM3"
BAUDRATE = 9600

def get_weight_from_load_cell():
    try:
        