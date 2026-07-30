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
        ctrlManager.update_controller_state(state, lock)
        #time.sleep(refresh_rate)

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

def display_thread(state, lock, stop_event, refresh_rate = 0.04):
    display = DisplayLive()
    while not stop_event.is_set():
        display.display_live(state, lock)
        time.sleep(refresh_rate)

def webserver_thread(state, lock, stop_event, refresh_rate = 0.04):
    WebServer(state).run()


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
        #threading.Thread(target=display_thread, args=(state, lock, stop_event))
        # threading.Thread(
        #     name="Web Server",
        #     target=webserver_thread, 
        #     args=(state, lock, stop_event), 
        #     daemon=True
        # )
    ]
   
    for t in threads:
        t.start()

    # def shutdown(signum, frame):
    #     logger.info("Shutdown requested")
    #     stop_event.set()

    # signal.signal(signal.SIGINT, shutdown)
    # signal.signal(signal.SIGTERM, shutdown)

    try:
        WebServer(state).run()
        #while True:
        #    time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Shutting down...")
        stop_event.set()

        for t in threads:
            if not t.daemon:
                t.join(timeout=10)

        logger.info("Shutdown complete.")

    

if __name__ == "__main__":
    main()