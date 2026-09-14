from interfaces.base_serial_driver import BaseSerialDriver
import logging
from logging_config import setup_logging

logger = logging.getLogger("dummy_serial_driver")

class DummySerialDriver(BaseSerialDriver):
    def __init__(self, port=None, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.last_command = None

    def write(self, data):
        self.last_command = data
        logger.debug(data.decode().strip())
 
    def close(self):
        logger.debug("Serial closed")