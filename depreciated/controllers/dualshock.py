import threading
import time
import hid

class DualShockController(threading.Thread):

    VID = 0x054C  # Sony
    PID = 0x0CE6  # DualSense USB (example)

    def __init__(self):

        super().__init__()

        self.device = None

        self.state = {
            "type": "ps5",
            "connected": False,
            "lx": 0,
            "ly": 0,
            "rx": 0,
            "ry": 0,
            "buttons": {}
        }

        self.lock = threading.Lock()

        self.stop_event = threading.Event()


    @staticmethod
    def available():

        devices = hid.enumerate()

        for d in devices:
            if (
                d["vendor_id"] == PS5Controller.VID
                and d["product_id"] == PS5Controller.PID
            ):
                return True

        return False


    def connect(self):

        devices = hid.enumerate()

        for d in devices:

            if (
                d["vendor_id"] == self.VID
                and d["product_id"] == self.PID
            ):

                self.device = hid.device()

                self.device.open_path(
                    d["path"]
                )

                return True

        return False


    def is_connected(self):

        with self.lock:
            return self.state["connected"]


    def get_state(self):

        with self.lock:
            return self.state.copy()


    def stop(self):

        self.stop_event.set()


    def run(self):

        while not self.stop_event.is_set():

            if self.device is None:

                connected = self.connect()

                with self.lock:
                    self.state["connected"] = connected


                if not connected:
                    time.sleep(2)
                    continue


            try:

                data = self.device.read(64)

                if data:

                    controller_state = self.parse(data)

                    with self.lock:
                        self.state.update(
                            controller_state
                        )


            except Exception:

                with self.lock:
                    self.state["connected"] = False

                self.device = None


            time.sleep(0.02)


    def parse(self, data):
         # DualSense HID parsing goes here

        return {
            "lx": data[1],
            "ly": data[2]
        }