class State:
    def __init__(self):
        #input state
        self.inputs = {}
        self.buttons = {

        }
        
        # self.sticks = {
        #     "lx": 0.0,
        #     "ly": 0.0,
        #     "rx": 0.0,
        #     "ry": 0.0
        # }
        
        # output state
        self.motors = {
            "left": 0,
            "right": 0,
        }

        # debug/raw state (optional)
        self.raw = {
            "source": None,
            "data": None,
            "timestamp": 0.0
        }

        self.telemetry = {
            "motor_output": None
        }