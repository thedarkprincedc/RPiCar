import time
import threading
import argparse
from state import State
from inputs.controller_manager import ControllerManager
from motor_controllers.motor_controller_factory import MotorControllerFactory
from interfaces.serial_driver_factory import SerialDriverFactory
from interfaces.serial_display import SerialDisplay
from interfaces.serial_telemetry import SerialTelemetry
from interfaces.serial_motor import SerialMotor
from telemetry.publisher import TelemetryPublisher
import logging
from logging_config import setup_logging
import json
from config import AppConfig

logger = logging.getLogger("main")

def usb_input_thread(state, lock, stop_event, config, refresh_rate = 0.005):
    ctrlManager = ControllerManager()
    while not stop_event.is_set():
        if not ctrlManager.has_controller():
            ctrlManager.scan()
            if not ctrlManager.has_controller():
                stop_event.wait(config.RPI_USB_CONTROLLER_SCAN_SECS)
                continue
        ctrlManager.update()
        with lock:
            state.inputs = ctrlManager.get_states()

def serial_thread(state, lock, stop_event, config, refresh_rate = 0.02):
    serial_display = SerialDisplay()
    serial_telemetry = SerialTelemetry()
    serial_motor = SerialMotor()

    serial_driver = SerialDriverFactory.create(config.RPI_SERIAL_DRIVER)
    logger.info(f"Created {serial_driver.__class__.__name__} Port: {serial_driver.port} Baudrate: {serial_driver.baudrate}")

    motor_controller = MotorControllerFactory.create(config.RPI_MOTOR_CONTROLLER_TYPE)
    logger.info(f"Created MotorControllerType: {motor_controller.__class__.__name__}")

    last_serial_telemetry_check = time.monotonic()
    last_serial_display_write = time.monotonic()

    while not stop_event.is_set():
        ctrl = None
        with lock:
            if state.inputs and state.inputs[0] is not None:
                ctrl = state.inputs[0]     

        if ctrl:
            motors = motor_controller.process_controller_input(ctrl)  
            serial_motor.write_motor(motors["left"], motors["right"], serial_driver)
            

        # Battery check every 2 minutes
        now = time.monotonic()
        #120
        if now - last_serial_telemetry_check >= config.RPI_SERIAL_TELEMETRY_CHECK_SECS:

            imu = serial_telemetry.imu_info(serial_driver)
            logger.debug(f"imu: {json.dumps(imu)}")

            ina = serial_telemetry.ina219_info(serial_driver)
            logger.debug(f"ina: {json.dumps(ina)}")

            last_serial_telemetry_check = now

        # print to screen
        if now - last_serial_display_write >= config.RPI_SERIAL_DISPLAY_WRITE_SECS:
            lines = [
                "RPiCar",
                "Waiting for controller",
                "Battery: 85%",
                "Speed: 0",
            ]
            serial_display.display(lines, serial_driver)
            last_serial_display_write = now

        time.sleep(refresh_rate)
    serial_driver.close()
    logger.debug("Serial closed")

def telemetry_thread(state, lock, stop_event, config, refresh_rate = 0.04):
    telemetryPublisher = TelemetryPublisher()
    while not stop_event.is_set():
        time.sleep(refresh_rate)

def create_car(debug=None):
    if debug is None:
        debug = AppConfig.DEBUG

    setup_logging(
        log_file="logs/main.log", 
        console_level=logging.DEBUG if debug else logging.INFO,
        log_to_file=True
    )

    state = State()
    lock = threading.Lock()
    stop_event = threading.Event()
    threads = [
        threading.Thread(
            target=usb_input_thread, 
            args=(state, lock, stop_event, AppConfig)
        ),
        threading.Thread(
            target=serial_thread, 
            args=(state, lock, stop_event, AppConfig)
        ),
        threading.Thread(
            target=telemetry_thread, 
            args=(state, lock, stop_event, AppConfig)
        )
    ]
    
    for thread in threads:
        thread.start()

    try:
        while not stop_event.wait(1):
            pass
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    finally:
        stop_event.set()
        logger.info("Waiting for threads to stop...")

        for thread in threads:
            thread.join(timeout=2)

        logger.info("Car stopped")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    create_car(args.debug)   

if __name__ == "__main__":
    main()