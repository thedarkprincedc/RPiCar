from interfaces.serial_driver import SerialDriver
import logging
from logging_config import setup_logging

logger = logging.getLogger(__name__)

class DummySerialDriver(SerialDriver):
    def __init__(self):
        self.last_command = None

    def write(self, data):
        self.last_command = data
        #logger.info("DUMMY SERIAL: " + data.decode().strip())
       
    def close(self):
        logger.info("Dummy serial closed")