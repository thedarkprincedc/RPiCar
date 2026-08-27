from interfaces.serial_driver import SerialDriver
import logging
from logging_config import setup_logging

logger = logging.getLogger("dummy_serial_driver")

class DummySerialDriver(SerialDriver):
    def __init__(self, port=None, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.last_command = None

    def write(self, data):
        self.last_command = data
        logger.debug(data.decode().strip())
       
    def close(self):
        logger.debug("Dummy Serial closed")
        pass

    def get_battery(self):
        logger.debug("battery voltage")
        return 0