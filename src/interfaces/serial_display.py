import json
import queue

class SerialDisplay:
    def __init__(self):
        self.queue = queue.Queue()

    def update(self, lines):
        """Request a display update."""
        self.queue.put(lines)

    def reset(self):
        """Request a display reset."""
        self.queue.put(None)

    def process(self, serial_driver):
        """Called by the serial thread."""
        try:
            lines = self.queue.get_nowait()
        except queue.Empty:
            return

        if lines is None:
            self._reset(serial_driver)
        else:
            self._display(lines, serial_driver)

    def _write_display(self, line_num, text, serial_driver):
        message = {
            "T": 3,
            "lineNum": line_num,
            "Text": text
        }

        serial_driver.write(
            (json.dumps(message) + "\n").encode()
        )

    def _reset(self, serial_driver):
        message = {"T": -3}

        serial_driver.write(
            (json.dumps(message) + "\n").encode()
        )

    def _display(self, lines, serial_driver):
        for line_num, line in enumerate(lines):
            self._write_display(line_num, line, serial_driver)
            
# class SerialDisplay:
#     def __init__(self):
#         self.last_serial_display_write = None

#     def write_display(self, line_num: int, text: str, serial_driver):
#         message = {
#             "T": 3,
#             "lineNum": line_num,
#             "Text": text
#         }

#         data = json.dumps(message) + "\n"
#         serial_driver.write(data.encode())

#     def reset(self, serial_driver):
#         message = {"T":-3}
#         data = json.dumps(message) + "\n"
#         serial_driver.write(data.encode())

#     def display(self, lines, serial_driver):
#         for line_num, line in enumerate(lines):
#             self.write_display(line_num, line, serial_driver)

    