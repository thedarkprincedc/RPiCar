from pynput import keyboard
import time

class KeyboardController:
    def __init__(self):
        self.keys = set()

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()

    def on_press(self, key):
        self.keys.add(str(key))

    def on_release(self, key):
        self.keys.discard(str(key))

    def parse(self):
        return {
            "dpad": {
                "up": 'Key.up' in self.keys,
                "right": 'Key.right' in self.keys,
                "down": 'Key.down' in self.keys,
                "left": 'Key.left' in self.keys,
            },
            "timestamp": time.time()
        }
    
def update_keyboard_state(state, lock, keyboard):
    data = keyboard.parse()
    if data:
        with lock:
            state.inputs['keyboard'] = data