from interfaces.base_serial_driver import BaseSerialDriver
import serial
import time
import logging
from logging_config import setup_logging

logger = logging.getLogger("serial_driver")

class SerialDriver(BaseSerialDriver):
    def __init__(self, port="/dev/serial0", baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.serial = serial.Serial(port, baudrate, timeout=0.01)

    def write(self, data):
        self.serial.write(data)
        logger.debug(data)

    def close(self):
        self.serial.close()

    def read_json(self, timeout=1.0):
        """
        Reads data from the serial port until the '}' character is encountered or until timeout.
        Parameters:
        timeout (float): Maximum time to wait for data in seconds.
        Returns:
        str: The data read from the serial port.
        """
        if not self.serial or not self.serial.is_open:
            print("Serial connection not established.")
            return ""

        start_time = time.time()
        read_data = ""
        while True:
            if time.time() - start_time > timeout:
                print("Read timeout.")
                break

            if self.serial.in_waiting > 0:
                char = self.serial.read().decode('utf-8')
                read_data += char
                if char == '}':
                    break

        return read_data