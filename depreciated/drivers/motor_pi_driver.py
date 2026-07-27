from drivers.motor_driver import MotorDriver

class RPiMotorDriver(MotorDriver):
    def __init__(self):
        import RPi.GPIO as GPIO
        self.IN1 = 17
        self.IN2 = 27
        self.ENA = 22

        self.IN3 = 23
        self.IN4 = 24
        self.ENB = 25

        GPIO.setmode(GPIO.BCM)

        GPIO.setup([self.IN1, self.IN2, self.IN3, self.IN4], GPIO.OUT)
        GPIO.setup([self.ENA, self.ENB], GPIO.OUT)

        self.pwmA = GPIO.PWM(self.ENA, 1000)
        self.pwmB = GPIO.PWM(self.ENB, 1000)

        self.pwmA.start(0)
        self.pwmB.start(0)

    def set_motor(self, left_dir, left_pwm, right_dir, right_pwm):
        # LEFT MOTOR direction
        GPIO.output(self.IN1, left_dir > 0)
        GPIO.output(self.IN2, left_dir <= 0)

        # RIGHT MOTOR direction
        GPIO.output(self.IN3, right_dir > 0)
        GPIO.output(self.IN4, right_dir <= 0)

        # speed (PWM)
        self.pwmA.ChangeDutyCycle(left_pwm * 100 / 255)
        self.pwmB.ChangeDutyCycle(right_pwm * 100 / 255)
