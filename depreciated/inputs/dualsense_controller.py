from inputs.base_controller import BaseController
import time

class DualSenseController(BaseController):
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
        
        if self.transport == "usb":
            return self.parse_usb(data)
        else:
            return self.parse_bluetooth(data)

    def parse_bluetooth(self, data):
        dpad = data[5] & 0x0F
        l2_analog = data[8]
        r2_analog = data[9]
        return {
            "dpad": {
                "up":    dpad in (0, 1, 7),
                "right": dpad in (1, 2, 3),
                "down":  dpad in (3, 4, 5),
                "left":  dpad in (5, 6, 7),
            },
            "sticks": {
                "lx": self.applyDeadZone(data[1]),
                "ly": self.applyDeadZone(data[2]),
                "rx": self.applyDeadZone(data[3]),
                "ry": self.applyDeadZone(data[4]),
            },
            "buttons": {
                # Byte 8: Action Buttons & D-Pad
                "square": bool(data[5] & 0x10),
                "cross": bool(data[5] & 0x20),
                "circle": bool(data[5] & 0x40),
                "triangle": bool(data[5] & 0x80),

                # Byte 9: Triggers, Shoulders, and System Menus
                "l1": bool(data[6] & 0x01),
                "r1": bool(data[6] & 0x02),
                "l2": bool(data[6] & 0x04),
                "r2": bool(data[6] & 0x08),
                "options": bool(data[6] & 0x0010),
                "create": bool(data[6] & 0x0020), # Share button
                "l3": bool(data[6] & 0x0040),
                "r3": bool(data[6] & 0x0080),

                # Byte 10: Center-Console Specialty Buttons
                "touchpad": bool(data[7] & 0x02),
                "ps": bool(data[7] & 0x01),
                #"mute": bool(data[8] & 0x04),
            },
            "triggers": {
                "l2_raw": l2_analog,
                "r2_raw": r2_analog,
                # Optional: Normalized percentage value (0.0 to 1.0)
                "l2_pct": round(l2_analog / 255.0, 2),
                "r2_pct": round(r2_analog / 255.0, 2),
            },

            "source": self.transport,
            "raw_data": data,
            "timestamp": time.time()
        }
    
    def parse_usb(self, data):
        dpad = data[8] & 0x0F
        l2_analog = data[5]
        r2_analog = data[6]
        return {
            "dpad": {
                "up":    dpad in (0, 1, 7),
                "right": dpad in (1, 2, 3),
                "down":  dpad in (3, 4, 5),
                "left":  dpad in (5, 6, 7),
            },
            "sticks": {
                "lx": self.applyDeadZone(data[1]),
                "ly": self.applyDeadZone(data[2]),
                "rx": self.applyDeadZone(data[3]),
                "ry": self.applyDeadZone(data[4]),
            },
            "buttons": {
                # Byte 8: Action Buttons & D-Pad
                "square": bool(data[8] & 0x10),
                "cross": bool(data[8] & 0x20),
                "circle": bool(data[8] & 0x40),
                "triangle": bool(data[8] & 0x80),

                # Byte 9: Triggers, Shoulders, and System Menus
                "l1": bool(data[9] & 0x01),
                "r1": bool(data[9] & 0x02),
                "l2": bool(data[9] & 0x04),
                "r2": bool(data[9] & 0x08),
                "options": bool(data[9] & 0x0010),
                "create": bool(data[9] & 0x0020), # Share button
                "l3": bool(data[9] & 0x0040),
                "r3": bool(data[9] & 0x0080),

                # Byte 10: Center-Console Specialty Buttons
                "touchpad": bool(data[10] & 0x02),
                "ps": bool(data[10] & 0x01),
                "mute": bool(data[10] & 0x04),
            },
            "triggers": {
                "l2_raw": l2_analog,
                "r2_raw": r2_analog,
                # Optional: Normalized percentage value (0.0 to 1.0)
                "l2_pct": round(l2_analog / 255.0, 2),
                "r2_pct": round(r2_analog / 255.0, 2),

            },
            # "raw": {
            #     "source": "usb",
            #     "data": data
            # },
            "source": self.transport,
            "raw_data": data,
            "timestamp": time.time()
        }
