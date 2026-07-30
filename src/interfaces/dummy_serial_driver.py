from interfaces.serial_driver import SerialDriver

class DummySerialDriver(SerialDriver):
    def __init__(self):
        self.last_command = None

    def write(self, data):
        self.last_command = data
        print("DUMMY SERIAL:", data.decode().strip())

    def close(self):
        print("Dummy serial closed")