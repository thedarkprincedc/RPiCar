from motor_controllers.motor_controller import MotorController
from motor_controllers.car_controller import MotorCarController
from motor_controllers.rc_controller import MotorRCController
from motor_controllers.tank_controller import MotorTankController

class MotorControllerFactory:
    CONTROLLER_TYPES = {
        "MotorController": MotorController,
        "MotorCarController": MotorCarController,
        "RCController": MotorRCController,
        "TankController": MotorTankController
    }

    @classmethod
    def create(cls, control_type: str | None = None):
        if control_type is None:
            control_type = "MotorController"
        try:
            controller_class = cls.CONTROLLER_TYPES[control_type]
        except KeyError:
            raise ValueError(
                f"Unknown motor controller: {control_type}"
            )
        return controller_class()