import platform
import time
import threading
import serial
import json
from controllers.manager import ControllerManager
from controllers.dualsense import DualSenseController
from controllers.dualshock import DualShockController
from controllers.xbox import XboxController
from serial_driver import RealSerialDriver, DummySerialDriver
from state import State




# def usb_input_thread(state, lock, stop_event, refresh_rate = 0.02):
#     print("starting: usb_input_thread")
#     while not stop_event.is_set():
#         data = update_controller_state()
#         if data:
#             with lock:
#                 state.inputs = data
#         time.sleep(refresh_rate)

def control_thread(state, lock, stop_event, controller_manager, refresh_rate = 0.02):
    print("starting: control_thread")
    while not stop_event.is_set():
        time.sleep(refresh_rate)

def serial_thread(state, lock, stop_event, serial_driver, refresh_rate = 0.02):
    print("starting: serial_thread")
    while not stop_event.is_set():
        with lock:
            if(state.inputs):
                command = {
                    "T": 1,
                    "L": state.motors["left"],
                    "R": state.motors["right"]
                }

                serial_driver.write((json.dumps(command) + "\n").encode())
                time.sleep(refresh_rate)
    serial_driver.close()

def display_thread(state, lock, stop_event, refresh_rate = 0.02):
    print("starting: display_thread")
    while not stop_event.is_set():
        time.sleep(refresh_rate)

def main():
    state = State()
    lock = threading.Lock()
    stop_event = threading.Event()

    # controller
    controller_manager = ControllerManager()
    controller_manager.register(DualSenseController())
    #controller_manager.register(DualShockController())
    #controller_manager.register(XboxController())
    #controller_manager.register(DummyController())
    controller_manager.auto_connect()

    thread = threading.Thread(
        target=controller_manager.run,
        args=(stop_event,),
    )

    thread.start()

    # serial driver
    if platform.system() == "Windows":
        serial_driver = DummySerialDriver()
    else:
        serial_driver = RealSerialDriver("/dev/serial0", 115200)

    threads = [
        # threading.Thread(target=control_thread, args=(state, lock, stop_event, controller_manager)),
        # threading.Thread(target=serial_thread, args=(state, lock, stop_event, serial_driver)),
        # threading.Thread(target=display_thread, args=(state, lock, stop_event))
    ]
    
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        stop_event.set()
        for t in threads:
            t.join()

if __name__ == "__main__":
    main()