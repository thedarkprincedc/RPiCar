import time
import threading
import os
import json
from state import State
from controller_manager import ControllerManager
from motor_controller import get_motor_driver, motor_control_data

def translate_controller_tank_drive_data(state, lock):
    with lock:
        if(state.inputs):
            input = state.inputs["1356:3302"]
           
            lx = input["sticks"]["lx"]
            ly = input["sticks"]["ly"]

            # simple tank drive mapping
            left  = ly + lx
            right = ly - lx

            # clamp
            left = max(-1, min(1, left))
            right = max(-1, min(1, right))

            state.motors["left"] = left
            state.motors["right"] = right

# threads 
# refresh_rate = 0.02 # 20ms
# refresh_rate = 0.05 # 50ms

def usb_input_thread(state, lock, stop_event, refresh_rate = 0.02):
    controllerManager = ControllerManager()
    controllers = controllerManager.scan()

    while not stop_event.is_set():
        for controller in controllers:
            data = controller.read()
            if data:
                with lock:
                    state.inputs[controller.id] = data
        time.sleep(refresh_rate)

def control_thread(state, lock, stop_event, refresh_rate = 0.02):
    while not stop_event.is_set():
        translate_controller_tank_drive_data(state, lock)
        time.sleep(refresh_rate)

def motor_thread(state, lock, stop_event, refresh_rate = 0.02):
    driver = get_motor_driver(state, lock)
    while not stop_event.is_set():
        motor_control_data(state, lock, driver)
        time.sleep(refresh_rate)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_live(state, lock, stop_event, refresh_rate = 0.05):
    while not stop_event.is_set():
        clear()

        with lock:
            #lx: {state.sticks['lx']:.2f} lx: {state.sticks['ly']:.2f}
            #rx: {state.sticks['rx']:.2f} rx: {state.sticks['ry']:.2f}
            clean = {
                cid: {
                    "sticks": data.get("sticks"),
                    "buttons": data.get("buttons"),
                    "timestamp": data.get("timestamp"),
                    "dpad": data.get("dpad"),
                    "triggers": data.get("triggers"),
                }
                for cid, data in state.inputs.items()
            }

            print(f"""
INPUT
inputs: {json.dumps(clean, indent=2)}

MOTORS
left: {state.motors['left']:.2f}
right: {state.motors['right']:.2f}

RAW SRC:


TELEMETRY:
motor_output: {state.telemetry["motor_output"]}
""")

        time.sleep(refresh_rate)


# -------------------------------
def main():
    state = State()
    stop_event = threading.Event()
    
    lock = threading.Lock()

    threads = [
        threading.Thread(target=usb_input_thread, args=(state, lock, stop_event)),
        threading.Thread(target=control_thread, args=(state, lock, stop_event)),
        threading.Thread(target=motor_thread, args=(state, lock, stop_event)),
        threading.Thread(target=display_live, args=(state, lock, stop_event))
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