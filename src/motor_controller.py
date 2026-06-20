import platform
from drivers.motor_pi_driver import RPiMotorDriver
from drivers.motor_mock_driver import MockMotorDriver

def to_pwm(x):
    return int(min(1.0, abs(x)) * 255)

def get_motor_driver(state, lock):
    if platform.system() == "Linux":
        try:
            return RPiMotorDriver()
        except ImportError:
            return MockMotorDriver(state, lock)
    else:
        print("running pc motor driver")
        return MockMotorDriver(state, lock)
    
def motor_control_data(state, lock, driver):
    with lock:
        left = state.motors["left"]
        right = state.motors["right"]

    # convert to hardware format
    left_dir = 1 if left >= 0 else -1
    right_dir = 1 if right >= 0 else -1

    left_pwm = to_pwm(left)
    right_pwm = to_pwm(right)
    driver.set_motor(left_dir, left_pwm, right_dir, right_pwm)
