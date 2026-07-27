import threading
import time


class ControllerManager:

    def __init__(self):
        self.devices = []
        self.device = None
        self.state = None
        self.lock = threading.Lock()

    def register(self, device):
        """
        Register an input device.

        Devices should implement:
            connect() -> bool
            disconnect()
            is_connected() -> bool
            update() -> ControllerState | None
        """
        self.devices.append(device)

    def auto_connect(self):
        """
        Try each registered device until one connects.
        """
        if self.device:
            self.device.disconnect()
            self.device = None

        for device in self.devices:
            try:
                if device.connect():
                    self.device = device
                    
                    print(f"Connected to {device.__class__.__name__}")
                    return True
            except Exception as ex:
                print(f"{device.__class__.__name__}: {ex}")

        print("No input devices available.")
        return False

    def set_device(self, device):
        """
        Force a specific device.
        """
        if self.device:
            self.device.disconnect()

        if device.connect():
            self.device = device
            return True

        return False

    def update(self):
        """
        Read the latest controller state.
        """
        if self.device is None:
            return

        # Lost controller?
        if not self.device.is_connected():
            print("Controller disconnected.")
            self.auto_connect()
            return

        state = self.device.update()

        if state is not None:
            with self.lock:
                self.state = state

    def get_state(self):
        with self.lock:
            return self.state

    def run(self, stop_event, refresh_rate=0.02):
        """
        Main thread loop.
        """
        while not stop_event.is_set():

            if self.device is None:
                self.auto_connect()

            self.update()

            time.sleep(refresh_rate)