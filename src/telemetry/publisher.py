import time

class TelemetryPublisher():
    def __init__(self, socketio, state):
        self.socketio = socketio
        self.state = state

    def run(self):
        while True:
            self.socketio.emit(
                "telemetry",
                self.state.data
            )
            time.sleep(0.5)
        
