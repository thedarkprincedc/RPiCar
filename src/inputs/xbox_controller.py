from inputs.base_controller import BaseController
from inputs.controller_state import ControllerState
import copy
import logging
from inputs.transports import get_bus_type_name

logger = logging.getLogger("xbox_controller")

class XboxController(BaseController):
    def __init__(self, device_info):
        super().__init__()
        self.device_info = device_info
        self.device = None
        self.transport = get_bus_type_name(device_info["bus_type"])
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
        config = self.transports[self.transport]
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

            product = device_info.get("product_string", "")

            if "XBOX" in product:
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
            logger.info(f"XBOX connection failed: {e}")
            return False

    def disconnect(self):
            return
    
    def update(self):
        data = self.device.read(self.report_size)

        if not data:
            return None
        
        self._state = self.parser(data)
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
            # analog
            "lx": int.from_bytes(data[10:12], byteorder='little', signed=True),
            "ly": int.from_bytes(data[12:14], byteorder='little', signed=True),
            "rx": int.from_bytes(data[14:16], byteorder='little', signed=True),
            "ry": int.from_bytes(data[16:18], byteorder='little', signed=True),
            # analog trigger

            #buttons
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
         
           
            # "lt": int.from_bytes(data[9:11], 'little'),
            # "rt": int.from_bytes(data[11:13], 'little')
        }