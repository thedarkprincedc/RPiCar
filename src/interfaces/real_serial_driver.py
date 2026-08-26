from interfaces.serial_driver import SerialDriver
import serial
import logging
from logging_config import setup_logging

logger = logging.getLogger("serial_driver")

class RealSerialDriver(SerialDriver):
    def __init__(self, port="/dev/serial0", baud=115200):
        self.serial = serial.Serial(
            port,
            baud,
            timeout=0.01
        )

    def write(self, data):
        self.serial.write(data)
        logger.debug(data)

    def close(self):
        self.serial.close()
        logger.debug("Serial closed")

    def get_battery(self):
        # Send the battery request to your controller
        self.serial.write(b"BATTERY\n")

        # Wait for response
        response = self.serial.readline()

        # Convert response to a value
        return int(response.decode().strip())