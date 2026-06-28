import time
import threading
from state import State
from controller_manager import ControllerManager, update_controller_state
from inputs.keyboard_controller import KeyboardController, update_keyboard_state
from display_live import display_live
from motor_controller import get_motor_driver, motor_control_data


def translate_controller_tank_drive_data(state, lock):
    with lock:
        if(state.inputs):
            # sets the input state to the first controller
            input = state.inputs[state.selected_ctrl_id]
           
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

def keyboard_input_thread(state, lock, stop_event, keyboard, refresh_rate = 0.02):
    while not stop_event.is_set():
        update_keyboard_state(state, lock, keyboard)
        time.sleep(refresh_rate)

def usb_input_thread(state, lock, stop_event, controllers, refresh_rate = 0.02):
    while not stop_event.is_set():
        update_controller_state(state, lock, controllers)
        time.sleep(refresh_rate)

def control_thread(state, lock, stop_event, refresh_rate = 0.02):
    while not stop_event.is_set():
        translate_controller_tank_drive_data(state, lock)
        time.sleep(refresh_rate)

def motor_thread(state, lock, stop_event, driver, refresh_rate = 0.02):
    while not stop_event.is_set():
        motor_control_data(state, lock, driver)
        time.sleep(refresh_rate)

def display_thread(state, lock, stop_event, refresh_rate = 0.04):
    while not stop_event.is_set():
        display_live(state, lock)
        time.sleep(refresh_rate)

# -------------------------------
def main():
    state = State()
    stop_event = threading.Event()
    lock = threading.Lock()

    controllerManager = ControllerManager()
    controllers = controllerManager.scan()
    state.selected_ctrl_id = controllerManager.get_firstcontroller()
    
    driver = get_motor_driver(state, lock)

    #kbd = KeyboardController()

    threads = [
       # threading.Thread(target=keyboard_input_thread, args=(state, lock, stop_event, kbd)),
        threading.Thread(target=usb_input_thread, args=(state, lock, stop_event, controllers)),
        threading.Thread(target=control_thread, args=(state, lock, stop_event)),
        threading.Thread(target=motor_thread, args=(state, lock, stop_event, driver)),
        threading.Thread(target=display_thread, args=(state, lock, stop_event))
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