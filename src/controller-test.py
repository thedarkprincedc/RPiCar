import platform
import time
import threading
from state import State
import hid
import os
import json
import serial

PS_PIDS = {
    0x09FC: "dualshock",
    0x09CC: "dualshock",
    0x0CE6: "dualsense",
    0x0DF2: "dualsense"
}

XBOX_PIDS = {
    0x02EA,
    0x02E0,  # Xbox One S Controller (example)
    0x0B13,  # Series X controller (example)
}

VENDORS = {
    0x045E: XBOX_PIDS,
    0x054C: PS_PIDS
}
class DualSenseController():
    def __init__(self, device, transport="usb"):
        self.device = device
        self.transport = transport
        self.dead_zone = 10     # tune this (usually 5-15)
        self.center = 128       # DS4 sticks rest near 128

    def applyDeadZone(self, value):
        diff = value - self.center

        if (abs(diff) < self.dead_zone):
            return 0.0;  # inside dead zone -> zero

        # Normalize to -1 to 1 range outside dead zone
        if(diff > 0):
            return (diff - self.dead_zone) / (127 - self.dead_zone)
        else:
            return (diff + self.dead_zone) / (128 - self.dead_zone)
    
    def read(self):
        data = self.device.read(78, timeout=5)
        #data = self.device.read(64, timeout=5)
        if not data:
            return None
        
        #return self.parse_usb(data)
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
                "lx": self.applyDeadZone(data[2] & 0xFF),
                "ly": self.applyDeadZone(data[3]),
                "rx": self.applyDeadZone(data[4]),
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
        }

class ControllerManager:
    def __init__(self):
        self.controllers = []

    def scan(self):
        devices = hid.enumerate()
        for d in devices:
            controller = self.create_controller(d)
            if controller:
                self.controllers.append(controller)
        return self.controllers
    
    def is_bluetooth(self, device):
        return device.get("bus_type") == hid.BusType.BLUETOOTH

    def create_controller(self, device):
        vid = device["vendor_id"]
        pid = device["product_id"]
        transport = "bluetooth" if self.is_bluetooth(device) == True else "usb"
        #transport = device.get("bus_type") == hid.BusType.BLUETOOTH
        
        if vid == 0x054C and pid in PS_PIDS:
           dev = hid.Device(vid, pid)
           kind = PS_PIDS.get(pid)
           if kind == "dualsense":
                controller = DualSenseController(dev, transport)
                return controller
        return None


    def update_controller_state(self, state, lock):
        for i, controller in enumerate(self.controllers):
            data = controller.read()
            if data:
                with lock:
                    state.inputs[i] = data


class SerialDriver:
    def write(self, data):
        raise NotImplementedError

    def close(self):
        pass

class RealSerialDriver(SerialDriver):
    def __init__(self, port="/dev/serial0", baud=115200):
        self.serial = serial.Serial(
            port,
            baud,
            timeout=0.01
        )

    def write(self, data):
        self.serial.write(data)

    def close(self):
        self.serial.close()

class DisplayLive():
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def display_live(self, state, lock):
        self.clear()
        with lock:
            print(json.dumps(state.inputs, indent=2))

class MotorController():
    def __init__(self):
        self.left = 0
        self.right = 0

    def apply_deadzone(self, value, deadzone=0.1):
        if abs(value) < deadzone:
            return 0
        return value

    def controller_to_motors(self, controller):
        # DualSense sticks
        forward = -controller["sticks"]["ly"]  # invert because up is negative
        turn = controller["sticks"]["lx"]

        forward = self.apply_deadzone(forward)
        turn = self.apply_deadzone(turn)

        # Tank drive mixing
        left = forward + turn
        right = forward - turn

        # Clamp to -1.0 -> 1.0
        left = max(-1, min(1, left))
        right = max(-1, min(1, right))

        return {
            "left": left,
            "right": right
        }

def serial_thread(state, lock, stop_event, refresh_rate = 0.02):
    serial_driver = RealSerialDriver("/dev/serial0", 115200)
    motor_controller = MotorController()
    while not stop_event.is_set():
        ctrl = None

        with lock:
            if state.inputs and state.inputs[0] is not None:
                ctrl = state.inputs[0]

        if ctrl:
            #print(json.dumps(state.inputs, indent=2))
            motors = motor_controller.controller_to_motors(ctrl)     
            command = f'{{"T":1,"L":{motors["left"]},"R":{motors["right"]}}}\n'
            serial_driver.write(command.encode())
        time.sleep(refresh_rate)
    serial_driver.close()

def usb_input_thread(state, lock, stop_event, refresh_rate = 0.005):
    ctrlManager = ControllerManager()
    ctrlManager.scan()

    while not stop_event.is_set():
        ctrlManager.update_controller_state(state, lock)
        #time.sleep(refresh_rate)

def display_thread(state, lock, stop_event, refresh_rate = 0.04):
    display = DisplayLive()
    while not stop_event.is_set():
        display.display_live(state, lock)
        time.sleep(refresh_rate)

def main():
    state = State()
    stop_event = threading.Event()
    lock = threading.Lock()

    threads = [
        threading.Thread(target=usb_input_thread, args=(state, lock, stop_event)),
        threading.Thread(target=serial_thread, args=(state, lock, stop_event)),
        #threading.Thread(target=display_thread, args=(state, lock, stop_event))
    ]
    
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Shutting down...")
        stop_event.set()
        for t in threads:
            t.join()

if __name__ == "__main__":
    main()