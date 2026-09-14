from inputs.base_controller import BaseController
from inputs.controller_state import ControllerState
from inputs.transports import get_bus_type_name
import copy
import logging

logger = logging.getLogger("dualshock_controller")

class DualShockController(BaseController):
    def __init__(self, device_info):
        super().__init__()
        self.device_info = device_info
        self.device = None
        self.transport = get_bus_type_name(device_info["bus_type"])
        self.connected = False
        self.dead_zone = 10     # tune this (usually 5-15)
        self.center = 128       # DS4 sticks rest near 128
        self.transports = {
            "BLUETOOTH": {
                "parser": self.parse_bluetooth, 
                "report_size": 64
            },
            "USB": {
                "parser": self.parse_usb,
                "report_size": 64
            }
        }
        config = self.transports[self.transport.upper()]
        self.parser = config["parser"]
        self.report_size = config["report_size"]
        self._state = ControllerState()

    @classmethod
    def scan(cls):
        controllers = []

        try:
            import hid
        except ImportError:
            logger.info("hid library not available")
            return controllers

        for device_info in hid.enumerate():
            vendor_id = device_info.get("vendor_id", "")
            product_id = device_info.get("product_id", "")
            if(vendor_id == 1356 or product_id == 2508):
                controllers.append(
                    cls(device_info)
                )

        return controllers

    def is_connected(self):
        return self.connected

    def connect(self):
        try:
            import hid
            self.device = hid.device()      
            
            logger.debug(", ".join([
                f"serial_number: {self.device_info["serial_number"]}",
                f"vid: {self.device_info["vendor_id"]}",
                f"pid: {self.device_info["product_id"]}"
            ]))
                  
            self.device.open_path(self.device_info["path"])
            self.connected = True
            self._state.connected = True
            return True
        except Exception as e:
            logger.error(f"DualShock connection failed: {e}")
            return False

    def disconnect(self):
        if self.device:
            try:
                self.device.close()
            except Exception as e:
                logger.warning("Error closing DualSense: %s", e)

        self.device = None
        self.connected = False

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
        if not self.device:
            return None
        try:
            data = self.device.read(self.report_size)
            self._state = self.parser(data)
            return True
        except Exception:
            self.disconnect()
            logger.warning("DualSense disconnected")
            return False

    def get_state(self):
        return copy.copy(self._state)

    def parse_bluetooth(self, data):
        return {
            # analog
            "lx": self.applyDeadZone(data[1]), 
            "ly": self.applyDeadZone(data[2]),
            "rx": self.applyDeadZone(data[3]), 
            "ry": self.applyDeadZone(data[4]),

            # buttons
            "square":     bool(data[5] & 0x10),
            "cross":      bool(data[5] & 0x20),
            "circle":     bool(data[5] & 0x40),
            "triangle":   bool(data[5] & 0x80),

            "l1":         bool(data[6] & 0x01),
            "r1":         bool(data[6] & 0x02),
            "l2digital":  bool(data[6] & 0x04),
            "r2digital":  bool(data[6] & 0x08),

            "options":    bool(data[6] & 0x20),
            "create":     bool(data[6] & 0x10),
            "l3":         bool(data[6] & 0x40),
            "r3":         bool(data[6] & 0x80),

            "ps":         bool(data[7] & 0x01),
            "touchpad":   bool(data[7] & 0x02),
        }
    
    def parse_usb(self, data):
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
            "square":     bool(data[5] & 0x10),
            "cross":      bool(data[5] & 0x20),
            "circle":     bool(data[5] & 0x40),
            "triangle":   bool(data[5] & 0x80),

            "l1":         bool(data[6] & 0x01),
            "r1":         bool(data[6] & 0x02),
            "l2digital":  bool(data[6] & 0x04),
            "r2digital":  bool(data[6] & 0x08),

            "options":    bool(data[6] & 0x20),
            "create":     bool(data[6] & 0x10),
            "l3":         bool(data[6] & 0x40),
            "r3":         bool(data[6] & 0x80),

            "ps":         bool(data[7] & 0x01),
            "touchpad":   bool(data[7] & 0x02),

            # "dpad": {
            #     "direction" : PS4_D_PAD_MAP[dpad]
            # },
        }



# PS4_D_PAD_MAP = {
#     8: 'neutral',
#     0: 'up',
#     1: 'upRight',
#     2: 'right',
#     3: 'downRight',
#     4: 'down',
#     5: 'downLeft',
#     6: 'left',
#     7: 'upLeft'
# }