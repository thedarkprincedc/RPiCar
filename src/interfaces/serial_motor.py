import json

class SerialMotor():
    def __init__(self):
        pass

    def write_motor(self, left: float, right: float, serial_driver):
        message = {
            "T": 1,
            "L": left,
            "R": right,
        }

        data = json.dumps(message) + "\n"
        serial_driver.write(data.encode())