import hid
from inputs.dualsense_controller import DualSenseController
from inputs.dualshock_controller import DualShockController
from inputs.xbox_controller import XboxController

PS_PIDS = {
    0x09CC: "dualshock",
    0x0CE6: "dualsense",
    0x0DF2: "dualsense"
}
XBOX_PIDS = {
    0x02E0,  # Xbox One S Controller (example)
    0x0B13,  # Series X controller (example)
}

class ControllerManager():
    def __init__(self):
        self.controllers = []

    def create_controller(self, device):
        vid = device["vendor_id"]
        pid = device["product_id"]
        name = (device.get("product_string") or "").lower()

        # Xbox (Microsoft VID)
        if vid == 0x045E and pid in XBOX_PIDS:
            return XboxController(device)
        
        # PlayStation (Sony VID)
        if vid == 0x054C and pid in PS_PIDS:
            dev = hid.Device(vid, pid)
            kind = PS_PIDS.get(pid)

            if kind == "dualshock":
                return DualShockController(dev)
            if kind == "dualsense":
                controller = DualSenseController(dev)
                controller.id = f"{vid}:{pid}"
                return controller 
        return None

    def scan(self):
        devices = hid.enumerate()

        for d in devices:
            controller = self.create_controller(d)
            if controller:
                self.controllers.append(controller)
        
        return self.controllers

