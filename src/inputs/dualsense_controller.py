from inputs.base_controller import BaseController
from inputs.controller_state import ControllerState
import copy
import logging
from inputs.transports import get_bus_type_name

logger = logging.getLogger("dualsense_controller")

class DualSenseController(BaseController):
    def __init__(self, device_info):
        super().__init__()
        self.device_info = device_info
        self.device = None
        self.transport = get_bus_type_name(device_info["bus_type"])
        self.connected = False
        self.dead_zone = 10     # tune this (usually 5-15)
        self.center = 128       # DS4 sticks rest near 128
        self.parsers = {
            "bluetooth": self.parse_bluetooth,
            "USB": self.parse_usb
        }
        self.report_sizes = {
            "bluetooth": 78,
            "USB": 64
        }
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

            product = device_info.get("product_string", "")

            if "DualSense" in product:
                controllers.append(
                    cls(device_info)
                )

        return controllers
    
    def connect(self):
        try:
            import hid
            self.device = hid.device()           
            self.device.open_path(self.device_info["path"])
         
            self._state.connected = True
            return True
        except Exception as e:
            logger.error(f"DualSense connection failed: {e}")
            return False

    def disconnect(self):
        if self.device:
            try:
                self.device.close()
            except Exception:
                logger.exception("Error closing DualSense")

        self.device = None
        self.connected = False
    
    def applyDeadZone(self, value):
        diff = value - self.center

        if (abs(diff) < self.dead_zone):
            return 0.0;  # inside dead zone -> zero

        # Normalize to -1 to 1 range outside dead zone
        if(diff > 0):
            return (diff - self.dead_zone) / (127 - self.dead_zone)
        else:
            return (diff + self.dead_zone) / (128 - self.dead_zone)

    def update(self):
        try:
            size = self.report_sizes[self.transport]
            data = self.device.read(size)
            
            if not data:
                return None
            
            self._state = self.parsers[self.transport](data)
            return self._state
        except Exception:
            self.disconnect()
            logger.warning("DualSense disconnected")
            return None
        
    
    def get_state(self):
        return copy.copy(self._state)
    
    def parse_bluetooth(self, data):
        dpad = data[5] & 0x0F
        l2_analog = data[8]
        r2_analog = data[9]
        return {
            # analog
            "lx": self.applyDeadZone(data[2] & 0xFF),
            "ly": self.applyDeadZone(data[3]),
            "rx": self.applyDeadZone(data[4]),
            "ry": self.applyDeadZone(data[4]),
            # analog trigger
            # "l2": bool(data[6] & 0x04),
            # "r2": bool(data[6] & 0x08),
            "l2": round(l2_analog / 255.0, 2),
            "r2": round(r2_analog / 255.0, 2),
            # hat switch

            # buttons
            #"square": bool(data[5] & 0x10),
            #"cross": bool(data[5] & 0x20),
            #"circle": bool(data[5] & 0x40),
            #"triangle": bool(data[5] & 0x80),

            "l1": bool(data[6] & 0x01),
            "r1": bool(data[6] & 0x02),
            "l3": bool(data[6] & 0x0040),
            "r3": bool(data[6] & 0x0080),

            "options": bool(data[6] & 0x0010),
            "create": bool(data[6] & 0x0020) # Share button
        }
        # return {
        #     "dpad": {
        #         "up":    dpad in (0, 1, 7),
        #         "right": dpad in (1, 2, 3),
        #         "down":  dpad in (3, 4, 5),
        #         "left":  dpad in (5, 6, 7),
        #     },
        #     "sticks": {
        #         "lx": self.applyDeadZone(data[2] & 0xFF),
        #         "ly": self.applyDeadZone(data[3]),
        #         "rx": self.applyDeadZone(data[4]),
        #         "ry": self.applyDeadZone(data[4]),
        #     },
        #     "buttons": {
        #         # Byte 8: Action Buttons & D-Pad
        #         "square": bool(data[5] & 0x10),
        #         "cross": bool(data[5] & 0x20),
        #         "circle": bool(data[5] & 0x40),
        #         "triangle": bool(data[5] & 0x80),

        #         # Byte 9: Triggers, Shoulders, and System Menus
        #         "l1": bool(data[6] & 0x01),
        #         "r1": bool(data[6] & 0x02),
        #         "l2": bool(data[6] & 0x04),
        #         "r2": bool(data[6] & 0x08),

        #         #
        #         "options": bool(data[6] & 0x0010),
        #         "create": bool(data[6] & 0x0020), # Share button
        #         "l3": bool(data[6] & 0x0040),
        #         "r3": bool(data[6] & 0x0080),

        #         # Byte 10: Center-Console Specialty Buttons
        #         "ps": bool(data[7] & 0x01),
        #         "touchpad": bool(data[7] & 0x02)
        #         #"mute": bool(data[8] & 0x04),
        #     },
        #     "triggers": {
        #         "l2_raw": l2_analog,
        #         "r2_raw": r2_analog,
        #         # Optional: Normalized percentage value (0.0 to 1.0)
        #         "l2_pct": round(l2_analog / 255.0, 2),
        #         "r2_pct": round(r2_analog / 255.0, 2),
        #     },
        # }
    
    def parse_usb(self, data):
        dpad = data[8] & 0x0F
        l2_analog = data[5]
        r2_analog = data[6]
        
        return {
            "up":    dpad in (0, 1, 7),
            "right": dpad in (1, 2, 3),
            "down":  dpad in (3, 4, 5),
            "left":  dpad in (5, 6, 7),
            # analog
            "lx": self.applyDeadZone(data[1]),
            "ly": self.applyDeadZone(data[2]),
            "rx": self.applyDeadZone(data[3]),
            "ry": self.applyDeadZone(data[4]),

            # analog trigger
            "l2": round(l2_analog / 255.0, 2),
            "r2": round(r2_analog / 255.0, 2),

            # buttons
            # Byte 8: Action Buttons & D-Pad
            "square": bool(data[8] & 0x10),
            "cross": bool(data[8] & 0x20),
            "circle": bool(data[8] & 0x40),
            "triangle": bool(data[8] & 0x80),

            # Byte 9: Triggers, Shoulders, and System Menus
            "l1": bool(data[9] & 0x01),
            "r1": bool(data[9] & 0x02),

            "l2digital": bool(data[9] & 0x04),
            "r2digital": bool(data[9] & 0x08),

            "options": bool(data[9] & 0x0010),
            "create": bool(data[9] & 0x0020), # Share button
            "l3": bool(data[9] & 0x0040),
            "r3": bool(data[9] & 0x0080),

            # Byte 10: Center-Console Specialty Buttons
            "ps": bool(data[10] & 0x01),
            "touchpad": bool(data[10] & 0x02),
            "mute": bool(data[10] & 0x04),
        }