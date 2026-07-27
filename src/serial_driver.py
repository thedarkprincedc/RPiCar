import serial
import time

class SerialDriver:
    def write(self, data):
        raise NotImplementedError

    def close(self):
        pass


class RealSerialDriver(SerialDriver):
    def __init__(self, port="/dev/serial0", baud=115200):
        self.serial = serial.Serial(
            port,
            baud,
            timeout=1
        )

    def write(self, data):
        self.serial.write(data)

    def close(self):
        self.serial.close()


class DummySerialDriver(SerialDriver):
    def __init__(self):
        self.last_command = None

    def write(self, data):
        self.last_command = data
        print("DUMMY SERIAL:", data.decode().strip())

    def close(self):
        print("Dummy serial closed")