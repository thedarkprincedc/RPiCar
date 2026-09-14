@dataclass
class TelemetryState:
    timestamp: float = 0

    battery_percent: float | None = None
    battery_voltage: float | None = None

    controller_connected: bool = False
    controller_type: str | None = None

    left_motor: float = 0.0
    right_motor: float = 0.0

    cpu_temperature: float | None = None

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "battery_percent": self.battery_percent,
            "battery_voltage": self.battery_voltage,
            "controller_connected": self.controller_connected,
            "controller_type": self.controller_type,
            "left_motor": self.left_motor,
            "right_motor": self.right_motor,
            "cpu_temperature": self.cpu_temperature,
        }