import hid
from inputs.dualsense_controller import DualSenseController
from inputs.dualshock_controller import DualShockController
from inputs.xbox_controller import XboxController

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

def is_bluetooth(device):
    return device.get("bus_type") == hid.BusType.BLUETOOTH

class ControllerManager():
    def __init__(self):
        self.controllers = []

    def create_controller(self, device):
        vid = device["vendor_id"]
        pid = device["product_id"]
        #name = (device.get("product_string") or "").lower()
        transport = "bluetooth" if is_bluetooth(device) == True else "usb"
        #print(vid)
       #print(pid)
        #print(device)
        #print(device["manufacturer_string"])
        # Xbox (Microsoft VID)
        #1356
        #2508

        if vid == 0x045E and pid in XBOX_PIDS:
            print("connecting to xbox controller")
            dev = hid.Device(vid, pid)
            controller = XboxController(dev, transport)
            controller.id = f"{vid}:{pid}"
            print(controller.id)
            return controller
        
        # PlayStation (Sony VID)
        if vid == 0x054C and pid in PS_PIDS:
            print("connecting to playstation controller")
            dev = hid.Device(vid, pid)
            kind = PS_PIDS.get(pid)

            if kind == "dualshock":
                print("connected to dualshock controller")
                controller = DualShockController(dev, transport)
                controller.id = f"{vid}:{pid}"
                return controller
            elif kind == "dualsense":
                controller = DualSenseController(dev, transport)
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
    
    def get_firstcontroller(self):
        if(self.controllers[0]):
            return self.controllers[0].id
        return 0
    
def update_controller_state(state, lock, controllers):
    for controller in controllers:
        data = controller.read()
        if data:
            with lock:
                state.inputs[controller.id] = data