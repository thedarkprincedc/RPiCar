import json

class SerialDisplay:
    def __init__(self):
        self.last_serial_display_write = None

    def write_display(self, line_num: int, text: str, serial_driver):
        message = {
            "T": 3,
            "lineNum": line_num,
            "Text": text
        }

        data = json.dumps(message) + "\n"
        serial_driver.write(data.encode())

    def reset(self, serial_driver):
        message = {"T":-3}
        data = json.dumps(message) + "\n"
        serial_driver.write(data.encode())

    def display(self, lines, serial_driver):
        for line_num, line in enumerate(lines):
            self.write_display(line_num, line, serial_driver)

    