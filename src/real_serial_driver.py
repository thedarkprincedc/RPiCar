from src.serial_driver import SerialDriver
import serial

class RealSerialDriver(SerialDriver):
    def __init__(self, port="/dev/serial0", baud=115200):
        self.serial = serial.Serial(
            port,
            baud,
            timeout=0.01
        )

    def write(self, data):
        self.serial.write(data)

    def close(self):
        self.serial.close()