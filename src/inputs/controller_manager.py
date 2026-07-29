import hid
from inputs.dualsense_controller import DualSenseController
from inputs.dualshock_controller import DualShockController
from inputs.xbox_controller import XboxController
import logging

logger = logging.getLogger(__name__)

CONTROLLERS = {
    (0x054C, 0x0CE6): DualSenseController,
    (0x054C, 0x09CC): DualShockController,
    (0x045E, 0x0B13): XboxController,
    # Add more controllers here
}

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

class ControllerManager:
    def __init__(self):
        self.controllers = []

    def scan(self):
        logger.info("Scanning controllers")
        devices = hid.enumerate()
        for d in devices:
            controller = self.create_controller(d)
            if controller:
                self.controllers.append(controller)
                logger.info("Connected %s", controller.__class__.__name__)
        return self.controllers
    
    def is_bluetooth(self, device):
        return device.get("bus_type") == hid.BusType.BLUETOOTH

    def get_transport(self, device):
        return "bluetooth" if self.is_bluetooth(device) == True else "usb"

    def create_controller(self, device):
        vid = device["vendor_id"]
        pid = device["product_id"]
        transport = self.get_transport(device)
        
        if vid == 0x054C and pid in PS_PIDS:
            dev = hid.Device(vid, pid)
            kind = PS_PIDS.get(pid)
            if kind == "dualsense":
                return DualSenseController(dev, transport)
            elif kind == "dualshock":
                return DualShockController(dev, transport)

        if vid == 0x045E and pid in XBOX_PIDS:
            return XboxController(dev, transport)

        return None


    def update_controller_state(self, state, lock):
        for i, controller in enumerate(self.controllers):
            data = controller.read()
            if data:
                with lock:
                    state.inputs[i] = data