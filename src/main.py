import time
import threading
from state import State
from inputs.controller_manager import ControllerManager
from drive.motor_controller import MotorController
from interfaces.real_serial_driver import RealSerialDriver
from web_server import WebServer
from display_live import DisplayLive
import logging
from logging_config import setup_logging
import signal

setup_logging()

logger = logging.getLogger(__name__)

def usb_input_thread(state, lock, stop_event, refresh_rate = 0.005):
    ctrlManager = ControllerManager()
    ctrlManager.scan()
    while not stop_event.is_set():
        ctrlManager.update()
        with lock:
            state.inputs = ctrlManager.get_states()

def serial_thread(state, lock, stop_event, refresh_rate = 0.02):
    serial_driver = RealSerialDriver("/dev/serial0", 115200)
    motor_controller = MotorController()
    while not stop_event.is_set():
        ctrl = None

        with lock:
            if state.inputs and state.inputs[0] is not None:
                ctrl = state.inputs[0]

        if ctrl:
            motors = motor_controller.controller_to_motors(ctrl)     
            command = f'{{"T":1,"L":{motors["left"]},"R":{motors["right"]}}}\n'
            serial_driver.write(command.encode())

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

def camera_thread(state, lock, stop_event, refresh_rate = 0.04):
    while not stop_event.is_set():            
        time.sleep(refresh_rate)


def main():
    logger.info("Starting RPiCar...")
    state = State()
    stop_event = threading.Event()
    lock = threading.Lock()

    threads = [
        threading.Thread(
            target=usb_input_thread, 
            args=(state, lock, stop_event)
        ),
        threading.Thread(
            target=serial_thread, 
            args=(state, lock, stop_event)
        ),
        threading.Thread(
            target=telemetry_thread, 
            args=(state, lock, stop_event)
        ),
        threading.Thread(
            target=camera_thread, 
            args=(state, lock, stop_event)
        )
    ]
   
    for t in threads:
        t.start()

    try:
        #WebServer(state).run()
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        stop_event.set()

        for t in threads:
            if not t.daemon:
                t.join(timeout=2)

        logger.info("Shutdown Complete...")

if __name__ == "__main__":
    main()