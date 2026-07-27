import os
import json

class DisplayLive():
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def display_live(self, state, lock):
        self.clear()
        with lock:
            print(json.dumps(state.inputs, indent=2))