class MotorTankController():
    def __init__(self):
        self.left = 0
        self.right = 0

    def apply_deadzone(self, value, deadzone=0.1):
        if abs(value) < deadzone:
            return 0
        return value

    def controller_to_motors(self, controller):
        left = controller["sticks"]["ly"]
        right = controller["sticks"]["ry"]

        # Clamp to -1.0 -> 1.0
        left = max(-1, min(1, left))
        right = max(-1, min(1, right))

        return {
            "left": left,
            "right": right
        }