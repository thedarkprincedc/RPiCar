from inputs.dualsense_controller import DualSenseController
from inputs.dualshock_controller import DualShockController
from inputs.xbox_controller import XboxController
from inputs.websocket_controller import WebSocketController
import logging

logger = logging.getLogger("controller_manager")

class ControllerManager:
    def __init__(self):
        self._controllers = []
        self.available_controllers = [
            XboxController,
            DualShockController,
            DualSenseController,
            #WebSocketController
        ]

    def has_controller(self):
        return len(self._controllers) > 0

    def register(self, controller):
        self._controllers.append(controller)
       
    def connect_all(self):
        for controller in self._controllers:
            if controller.connect():
                logger.info(f"{controller.__class__.__name__} connected")

    def update(self):
        for controller in self._controllers:
            controller.update()

    def get_states(self):
        return [
            controller.get_state()
            for controller in self._controllers
        ]   

    def scan(self):
        logger.info("Waiting for controller...")
        for controller_type in self.available_controllers:
            controllers = controller_type.scan()
            logger.debug(f"Scanned {controller_type.__name__}")
            for controller in controllers:
                if controller.connect():
                    logger.info(f"Connected {controller_type.__name__}")
                    self.register(controller)
                    logger.info(f"Registered {controller.__class__.__name__}")
                    return