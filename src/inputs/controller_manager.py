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
            DualSenseController,
            DualShockController,
            XboxController,
            WebSocketController
        ]

    def has_controller(self):
        return bool(self._controllers)

    def register(self, controller):
        self._controllers.append(controller)
        logger.info(f"{controller.__class__.__name__} registered")

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
        for controller_type in self.available_controllers:
            controllers = controller_type.scan()
            logger.info(controller_type.__name__)
            for controller in controllers:
                if controller.connect():
                    self.register(controller)