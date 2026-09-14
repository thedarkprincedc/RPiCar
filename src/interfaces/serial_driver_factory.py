from interfaces.serial_driver import SerialDriver
from interfaces.dummy_serial_driver import DummySerialDriver
import platform

class SerialDriverFactory:
    @staticmethod
    def create(driver_type: str | None = None, port: str = "/dev/serial0", baudrate: int = 115200):
        if driver_type is None:
            system = platform.system()

            if system == "Linux":
                driver_type = "real"
            elif system in ("Windows", "Darwin"):
                driver_type = "dummy"
            else:
                raise RuntimeError(
                    f"Unsupported platform: {system}"
                )

        if driver_type == "real":
            return SerialDriver(
                port=port,
                baudrate=baudrate,
            )

        if driver_type == "dummy":
            return DummySerialDriver(
                port=port,
                baudrate=baudrate,
            )

        raise ValueError(
            f"Unknown serial driver type: {driver_type}"
        )
    