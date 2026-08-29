
import platform
import logging
from logging_config import setup_logging
import argparse
from ble_manager import setup_bluetooth_linux

logger = logging.getLogger("main")

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    setup_logging(
        log_file="logs/ble.log", 
        console_level=logging.DEBUG if args.debug else logging.INFO
    )

    logger.info("Starting Bluetooth Setup...")

    if(platform.system() == "Linux"):
        setup_bluetooth_linux()
    else:
        logger.info(f"{platform.system()} is not supported by bluetooth manager")
    
    logger.info("Ending Bluetooth Setup...")

if __name__ == "__main__":
    main()