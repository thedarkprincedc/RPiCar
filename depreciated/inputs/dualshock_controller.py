from inputs.base_controller import BaseController
import time

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
    def __init__(self, device, transport="usb"):
        self.device = device
        self.transport = transport
        self.dead_zone = 10     # tune this (usually 5-15)
        self.center = 128       # DS4 sticks rest near 128
        
    def applyDeadZone(self, value):
        diff = value - self.center

        if (abs(diff) < self.dead_zone):
            return 0;  # inside dead zone -> zero

        # Normalize to -1 to 1 range outside dead zone
        if(diff > 0):
            return (diff - self.dead_zone) / (127 - self.dead_zone)
        else:
            return (diff + self.dead_zone) / (127 - self.dead_zone)
        
    def read(self):
        data = self.device.read(64)
        if not data:
            return None
        return self.parse(data)

    def parse(self, data):
        dpad = data[5] & 0x0F
        return {
            "dpad": {
                "direction" : PS4_D_PAD_MAP[dpad]
            },
            "sticks": {
                "lx": self.applyDeadZone(data[1]), 
                "ly": self.applyDeadZone(data[2]),
                "rx": self.applyDeadZone(data[3]), 
                "ry": self.applyDeadZone(data[4])
            },
            "buttons": {
                "square":   bool(data[5] & 0x10),
                "cross":    bool(data[5] & 0x20),
                "circle":   bool(data[5] & 0x40),
                "triangle": bool(data[5] & 0x80),

                "l1":      bool(data[6] & 0x01),
                "r1":      bool(data[6] & 0x02),
                "l2":      bool(data[6] & 0x04),
                "r2":      bool(data[6] & 0x08),
                "share":   bool(data[6] & 0x10),
                "options": bool(data[6] & 0x20),
                "l3":      bool(data[6] & 0x40),
                "r3":      bool(data[6] & 0x80),

                "ps":       bool(data[7] & 0x01),
                "touchpad": bool(data[7] & 0x02),
            },
            "triggers": {
                "l2": data[8], 
                "r2": data[9]
            },
            "source": self.transport,
            "raw_data": data,
            "timestamp": time.time()
        }