from inputs.base_controller import BaseController
from inputs.controller_state import ControllerState
import copy
import logging
from inputs.transports import get_bus_type_name

logger = logging.getLogger("dualshock_controller")

PS4_D_PAD_MAP = {
    8: 'neutral',
    0: 'up',
    1: 'upRight',
    2: 'right',
    3: 'downRight',
    4: 'down',
    5: 'downLeft',
    6: 'left',
    7: 'upLeft'
}

class DualShockController(BaseController):
    def __init__(self, device_info):
        super().__init__()
        self.device_info = device_info
        self.device = None
        self.transport = get_bus_type_name(device_info["bus_type"])
        self.dead_zone = 10     # tune this (usually 5-15)
        self.center = 128       # DS4 sticks rest near 128
        self.parser = {
            "bluetooth": self.parse_bluetooth,
            "USB": self.parse_usb
        }
        self.report_sizes = {
            "bluetooth": 64,
            "USB": 64
        }
        self._state = ControllerState()

    @classmethod
    def scan(cls):
        controllers = []
        BUS_TYPES = {
            0: "Unknown",
            1: "USB",
            2: "Bluetooth",
            3: "I2C",
            4: "SPI",
        }

        try:
            import hid
        except ImportError:
            logger.info("hid library not available")
            return controllers

        for device_info in hid.enumerate():

            product = device_info.get("product_string", "")

            if "DualShock" in product:
                print(f"Found DualShock: {product}")

                controllers.append(
                    cls(device_info)
                )

        return controllers

    def connect(self):
        try:
            import hid
            self.device = hid.device()           
            self.device.open_path(self.device_info["path"])

            #self._state.connected = True
            print("DualShock connected")
            return True
        except Exception as e:
            logger.error(f"DualShock connection failed: {e}")
            return False

    def disconnect(self):
        return

    def applyDeadZone(self, value):
        diff = value - self.center

        if (abs(diff) < self.dead_zone):
            return 0;  # inside dead zone -> zero

        # Normalize to -1 to 1 range outside dead zone
        if(diff > 0):
            return (diff - self.dead_zone) / (127 - self.dead_zone)
        else:
            return (diff + self.dead_zone) / (127 - self.dead_zone)
        
    def update(self):
        size = self.report_sizes[self.transport]
        data = self.device.read(size)
        
        if not data:
            return None
        self._state = self.parsers[self.transport](data)
        return self._state

    def get_state(self):
        return copy.copy(self._state)

    def parse_bluetooth(self, data):
        return self.parse(data)
    
    def parse_usb(self, data):
        return self.parse(data)

    def parse(self, data):
        return {
            # analog
            "lx": self.applyDeadZone(data[1]), 
            "ly": self.applyDeadZone(data[2]),
            "rx": self.applyDeadZone(data[3]), 
            "ry": self.applyDeadZone(data[4]),

            # analog trigger
            "l2": data[8], 
            "r2": data[9],

            # buttons
            "square":   bool(data[5] & 0x10),
            "cross":    bool(data[5] & 0x20),
            "circle":   bool(data[5] & 0x40),
            "triangle": bool(data[5] & 0x80),

            "l1":      bool(data[6] & 0x01),
            "r1":      bool(data[6] & 0x02),
            "l2digital":      bool(data[6] & 0x04),
            "r2digital":      bool(data[6] & 0x08),

            "options": bool(data[6] & 0x20),
            "create":   bool(data[6] & 0x10),
            "l3":      bool(data[6] & 0x40),
            "r3":      bool(data[6] & 0x80),

            "ps":       bool(data[7] & 0x01),
            "touchpad": bool(data[7] & 0x02),

            # "dpad": {
            #     "direction" : PS4_D_PAD_MAP[dpad]
            # },
        }