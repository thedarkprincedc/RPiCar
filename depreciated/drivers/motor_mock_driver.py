from drivers.motor_driver import MotorDriver

class MockMotorDriver(MotorDriver):
    def __init__(self, state=None, lock=None):
        self.state = state
        self.lock = lock

    def set_motor(self, left_dir, left_pwm, right_dir, right_pwm):
        if self.state and self.lock:
            with self.lock:
                self.state.telemetry["motor_output"] = {
                    "left_pwm": left_pwm,
                    "right_pwm": right_pwm,
                    "left_dir": left_dir,
                    "right_dir": right_dir
                }
