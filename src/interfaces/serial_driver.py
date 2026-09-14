from interfaces.base_serial_driver import BaseSerialDriver
import serial
import logging
from logging_config import setup_logging

logger = logging.getLogger("serial_driver")

class SerialDriver(BaseSerialDriver):
    def __init__(self, port="/dev/serial0", baudrate=115200):
        self.serial = serial.Serial(port, baudrate, timeout=0.01)

    def write(self, data):
        self.serial.write(data)
        logger.debug(data)

    def close(self):
        self.serial.close()
        logger.debug("Serial closed")