from inputs.base_controller import BaseController
from inputs.controller_state import ControllerState
import copy
import logging

logger = logging.getLogger("xbox_controller")

class XboxController(BaseController):
    def __init__(self, device, transport="usb"):
        super().__init__()
        self.device = device
        self.transport = transport
        self.parsers = {
            "bluetooth": self.parse_bluetooth,
            "usb": self.parse_usb
        }
        self.report_sizes = {
            "bluetooth": 64,
            "usb": 64
        }
        self._state = ControllerState()

    @classmethod
    def scan(cls):
        controllers = []

        try:
            import hid
        except ImportError:
            #logger.info("hid library not available")
            return controllers

        for device in hid.enumerate():

            product = device.get("product_string", "")

            if "XBOX" in product:
                print(f"Found XBOX: {product}")
                transport = "bluetooth" if device.get("bus_type") == hid.BusType.BLUETOOTH else "usb"
                controllers.append(
                    cls(device, transport)
                )

        return controllers

    def connect(self):
        try:
            import hid
            self.device = hid.Device(self.device["vendor_id"], self.device["product_id"])
            #self._state.connected = True
            print("XBOX connected")
            return True
        except Exception as e:
            print(f"XBOX connection failed: {e}")
            return False

    def disconnect(self):
            return
    
    def update(self):
        size = self.report_sizes[self.transport]
        data = self.device.read(size, timeout=5)

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
        buttons_byte = data[2]
        return {
            "dpad": {},
            "sticks": {
                "lx": int.from_bytes(data[10:12], byteorder='little', signed=True),
                "ly": int.from_bytes(data[12:14], byteorder='little', signed=True),
                "rx": int.from_bytes(data[14:16], byteorder='little', signed=True),
                "ry": int.from_bytes(data[16:18], byteorder='little', signed=True)
            },
            "buttons": {
                "a":      bool(buttons_byte & (1 << 4)),
                "b":      bool(buttons_byte & (1 << 5)),
                "x":      bool(buttons_byte & (1 << 6)),
                "y":      bool(buttons_byte & (1 << 7))
                # "b":       { byte: 14, mask: 0x02},
                # "x":       { byte: 14, mask: 0x08},
                # "y":       { byte: 14, mask: 0x10},
                # "lb":      { byte: 14, mask: 0x40},
                # "rb":      { byte: 14, mask: 0x80},
                # "lt":      { },
                # "rt":      { },
                # "view":    { byte: 15, mask: 0x04},
                # "options": { byte: 15, mask: 0x08},
                # "xbox":    { byte: 15, mask: 0x10},
                # "ltb":     { byte: 15, mask: 0x20},
                # "rtb":     { byte: 15, mask: 0x40},
                # "share":   { byte: 16, mask: 0x01}
            },
            "triggers": {
                "lt": int.from_bytes(data[9:11], 'little'),
                "rt": int.from_bytes(data[11:13], 'little')
            },
        }