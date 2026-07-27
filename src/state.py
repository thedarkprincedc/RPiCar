class State:
    def __init__(self):
        #input state
        self.inputs = [None]
        
        # output state
        self.motors = {
            "left": 0.0,
            "right": 0.0,
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