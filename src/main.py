import time
import threading
from state import State
from inputs.controller_manager import ControllerManager
from real_serial_driver import RealSerialDriver
from motor_controller import MotorController
from display_live import DisplayLive
import json

def usb_input_thread(state, lock, stop_event, refresh_rate = 0.005):
    print("usb_input_thread")
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
            #print(json.dumps(state.inputs, indent=2))
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

def main():
    state = State()
    stop_event = threading.Event()
    lock = threading.Lock()

    threads = [
        threading.Thread(target=usb_input_thread, args=(state, lock, stop_event)),
        threading.Thread(target=serial_thread, args=(state, lock, stop_event)),
        #threading.Thread(target=display_thread, args=(state, lock, stop_event))
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