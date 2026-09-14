from enum import Enum

BUS_TYPES = {
    0: "Unknown",
    1: "USB",
    2: "Bluetooth",
    3: "I2C",
    4: "SPI",
}

def get_bus_type_name(busType):
    return BUS_TYPES[busType]

