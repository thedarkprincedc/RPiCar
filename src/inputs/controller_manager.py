#import hid
from inputs.dualsense_controller import DualSenseController
from inputs.dualshock_controller import DualShockController
from inputs.xbox_controller import XboxController
import logging

logger = logging.getLogger(__name__)

# CONTROLLERS = {
#     (0x054C, 0x0CE6): DualSenseController,
#     (0x054C, 0x09CC): DualShockController,
#     (0x045E, 0x0B13): XboxController,
#     # Add more controllers here
# }

# PS_PIDS = {
#     0x09FC: "dualshock",
#     0x09CC: "dualshock",
#     0x0CE6: "dualsense",
#     0x0DF2: "dualsense"
# }

# XBOX_PIDS = {
#     0x02EA,
#     0x02E0,  # Xbox One S Controller (example)
#     0x0B13,  # Series X controller (example)
# }

# VENDORS = {
#     0x045E: XBOX_PIDS,
#     0x054C: PS_PIDS
# }

class ControllerManager:
    def __init__(self):
        self._controllers = []
        self._state = None

    def register(self, controller):
        self._controllers.append(controller)

    def connect_all(self):
        for controller in self._controllers:
            if controller.connect():
                print(f"{controller.__class__.__name__} connected")

    def update(self):
        for controller in self._controllers:
            controller.update()
            #print(controller._state)

    def get_states(self):
        return [
            controller.get_state()
            for controller in self._controllers
        ]   

    def scan(self):
        AVAILABLE_CONTROLLERS = [
            DualSenseController,
           # XboxController
        ]
        for controller_type in AVAILABLE_CONTROLLERS:
            controllers = controller_type.scan()

            for controller in controllers:
                if controller.connect():
                    self.register(controller)

    # def scan2(self):
    #     controller_types = [
    #         DualSenseController,
    #         XboxController
    #     ]
        
    #     for controller_type in controller_types:
    #        found = controller_type.scan() 
    #        for controller in found:
    #             if controller.connect():
    #                 self.controllers.append(controller)

    #     logger.info(f"Found {len(self.controllers)} controllers")

    #     return self.controllers

    # def scan(self):
    #     logger.info("Scanning controllers")
    #     devices = hid.enumerate()
    #     for d in devices:
    #         controller = self.create_controller(d)
    #         if controller:
    #             self.controllers.append(controller)
    #             logger.info("Connected %s", controller.__class__.__name__)
    #     return self.controllers
    
    # def is_bluetooth(self, device):
    #     return device.get("bus_type") == hid.BusType.BLUETOOTH

    # def get_transport(self, device):
    #     return "bluetooth" if self.is_bluetooth(device) == True else "usb"

    # def create_controller(self, device):
    #     vid = device["vendor_id"]
    #     pid = device["product_id"]
    #     transport = self.get_transport(device)
        
    #     if vid == 0x054C and pid in PS_PIDS:
    #         dev = hid.Device(vid, pid)
    #         kind = PS_PIDS.get(pid)
    #         if kind == "dualsense":
    #             return DualSenseController(dev, transport)
    #         elif kind == "dualshock":
    #             return DualShockController(dev, transport)

    #     if vid == 0x045E and pid in XBOX_PIDS:
    #         return XboxController(dev, transport)

    #     return None


    # def update_controller_state(self, state, lock):
    #     for i, controller in enumerate(self.controllers):
    #         data = controller.read()
    #         if data:
    #             with lock:
    #                 state.inputs[i] = data

    # def update(self):
    #     for controller in self.controllers:
    #         try:
    #             controller.update()
    #             # self.states[controller.name] = (
    #             #     controller.get_state()
    #             # )
    #         except Exception as e:
    #             print(
    #                 f"{controller.name} update failed: {e}"
                # )