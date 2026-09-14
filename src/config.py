import os
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class AppConfig:
    """A central hub for all project configurations."""
    # variables
    RPI_PORT = os.getenv("PORT") or 5000
    # directories
    RPI_LOG_DIR = os.getenv("LOG_DIR") or Path("./logs").resolve()
    RPI_TEMPLATE_DIR = os.getenv("TEMPLATE_DIR") or Path("./src/web/templates").resolve()
    RPI_STATIC_DIR = os.getenv("STATIC_DIR") or Path("./src/web/static").resolve()
    # paths
    RPI_LOG_PATH = os.getenv("LOG_PATH") or RPI_LOG_DIR / "main.log"
    #
    RPI_USB_CONTROLLER_SCAN_SECS = 1.5
    RPI_SERIAL_DRIVER = None
    RPI_MOTOR_CONTROLLER_TYPE = None
    RPI_SERIAL_TELEMETRY_CHECK_SECS = 5
    RPI_SERIAL_DISPLAY_WRITE_SECS = 4
    

    DEBUG = os.getenv("DEBUG", "false").lower() == "true"