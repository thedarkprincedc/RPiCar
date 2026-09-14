from motor_controllers.base_motor_controller import BaseMotorController

class MotorCarController(BaseMotorController):
    def __init__(self):
        self.left = 0
        self.right = 0

    def process_controller_input(self, controller):
        reverse = controller["triggers"]["l2_pct"]
        forward = controller["triggers"]["r2_pct"]
        turn = controller["sticks"]["lx"]

        left = (reverse + forward) + turn
        right = (reverse + forward) - turn

        # Clamp to -1.0 -> 1.0
        left = max(-1, min(1, left))
        right = max(-1, min(1, right))

        return {
            "left": left,
            "right": right
        }