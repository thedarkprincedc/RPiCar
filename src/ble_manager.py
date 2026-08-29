from btpy import ClassicDevice, LEDevice
import logging

logger = logging.getLogger("ble_manager")

def setup_bluetooth_linux():
    # 1. Scan for Bluetooth Classic Devices (e.g., PS4/PS5 controllers, older speakers)
    logger.info("Scanning for Classic devices...")
    classic_devices = ClassicDevice.scan(5)
    for device in classic_devices:
        logger.info(f"[Classic] Found: {device.name} ({device.address})")

    # 2. Scan for BLE Devices (e.g., Updated Xbox controllers, IoT sensors)
    logger.info("Scanning for BLE devices...")
    ble_devices = LEDevice.scan(5)
    for device in ble_devices:
        logger.info(f"[BLE] Found: {device.name} ({device.address})")