from inputs.base_controller import BaseController
import time

class XboxController(BaseController):
    def __init__(self, device, transport="usb"):
        self.device = device
        self.transport = transport
        
    def read(self):
        data = self.device.read(64)
        if not data:
            return None
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
            "source": self.transport,
            "raw_data": data,
            "timestamp": time.time()
        }