from interfaces.base_serial_driver import BaseSerialDriver
import serial
import time
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

    def read_json(self, serial_driver, timeout=1.0):
        """
        Reads data from the serial port until the '}' character is encountered or until timeout.
        Parameters:
        timeout (float): Maximum time to wait for data in seconds.
        Returns:
        str: The data read from the serial port.
        """
        if not self.serial.serial_connection or not self.serial.serial_connection.is_open:
            print("Serial connection not established.")
            return ""

        start_time = time.time()
        read_data = ""
        while True:
            if time.time() - start_time > timeout:
                print("Read timeout.")
                break

            if serial_driver.serial_connection.in_waiting > 0:
                char = self.serial.serial_connection.read().decode('utf-8')
                read_data += char
                if char == '}':
                    break

        return read_data