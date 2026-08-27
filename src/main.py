import time
import threading
from state import State
from inputs.controller_manager import ControllerManager
from drive.motor_controller import MotorController
from interfaces.serial_factory import create_serial_driver
from display_live import DisplayLive
import logging
from logging_config import setup_logging
import argparse

logger = logging.getLogger("main")

def usb_input_thread(state, lock, stop_event, refresh_rate = 0.005):
    ctrlManager = ControllerManager()
    while not stop_event.is_set():
        if not ctrlManager.has_controller():
            ctrlManager.scan()
            if not ctrlManager.has_controller():
                stop_event.wait(1.0)
                continue

        ctrlManager.update()
        with lock:
            state.inputs = ctrlManager.get_states()

def serial_thread(state, lock, stop_event, serial_driver, refresh_rate = 0.02):
    motor_controller = MotorController()
    last_battery_check = time.monotonic()
    while not stop_event.is_set():
        ctrl = None

        with lock:
            if state.inputs and state.inputs[0] is not None:
                ctrl = state.inputs[0]

        if ctrl:
            motors = motor_controller.controller_to_motors(ctrl)     
            command = f'{{"T":1,"L":{motors["left"]},"R":{motors["right"]}}}\n'
            serial_driver.write(command.encode())

        # Battery check every 2 minutes
        now = time.monotonic()

        if now - last_battery_check >= 120:
            battery = serial_driver.get_battery()

            with lock:
                state.battery = battery

            last_battery_check = now

        time.sleep(refresh_rate)
    serial_driver.close()

# def display_thread(state, lock, stop_event, refresh_rate = 0.04):
#     display = DisplayLive()
#     while not stop_event.is_set():
#         display.display_live(state, lock)
#         time.sleep(refresh_rate)

def telemetry_thread(state, lock, stop_event, refresh_rate = 0.04):
    while not stop_event.is_set():
        time.sleep(refresh_rate)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    # parser.add_argument(
    #     "--debug",
    #     action="store_true",
    #     default="logs/main.log"
    #     help="Enable debug logging",
    # )

    args = parser.parse_args()

    setup_logging(
        log_file="logs/main.log", 
        console_level=logging.DEBUG if args.debug else logging.INFO
    )
    
    logger.info("Starting RPiCar...")
    state = State()
    stop_event = threading.Event()
    lock = threading.Lock()

    serial_driver = create_serial_driver("/dev/serial0", 115200)
    logger.info(f"Created {serial_driver.__class__.__name__} Port: {serial_driver.port} Baudrate: {serial_driver.baudrate}")
    
    threads = [
        threading.Thread(
            target=usb_input_thread, 
            args=(state, lock, stop_event)
        ),
        threading.Thread(
            target=serial_thread, 
            args=(state, lock, stop_event, serial_driver)
        ),
        threading.Thread(
            target=telemetry_thread, 
            args=(state, lock, stop_event)
        )
    ]
   
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        stop_event.set()
        for t in threads:
            if not t.daemon:
                t.join(timeout=2)

        logger.info("Shutdown RPiCar...")

if __name__ == "__main__":
    main()