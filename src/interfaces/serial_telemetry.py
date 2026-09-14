import json

class SerialTelemetry:
    def __init__(self):
        pass

    def ina219_info(self, serial_driver):
        """
        Gets information about the INA219, including the voltage and current power of the power supply.
        """
        command = {"T": 130}
        serial_driver.write(
            (json.dumps(command) + "\n").encode()
        )
        return serial_driver.read_json()

    
    def imu_info(self, serial_driver):
        """
        Obtains IMU information, including heading angle, geomagnetic field, acceleration, attitude, temperature, etc.
        """
        command = {"T": 126}
        serial_driver.write(
            (json.dumps(command) + "\n").encode()
        )
        return serial_driver.read_json()