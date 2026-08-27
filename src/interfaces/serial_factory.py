import platform
from .real_serial_driver import RealSerialDriver
from .dummy_serial_driver import DummySerialDriver

DRIVERS = {
    "Linux": RealSerialDriver,
    "Windows": DummySerialDriver,
}

def create_serial_driver(*args, **kwargs):
    system = platform.system()

    try:
        driver_class = DRIVERS[system]
    except KeyError:
        raise RuntimeError(f"Unsupported operating system: {system}")

    return driver_class(*args, **kwargs)