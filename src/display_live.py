import os
import json

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_live(state, lock):
    clear()

    with lock:
        clean = {
            cid: {
                "sticks": data.get("sticks"),
                "buttons": data.get("buttons"),
                "dpad": data.get("dpad"),
                "triggers": data.get("triggers"),
                "source": data.get("source"),
                "timestamp": data.get("timestamp"),
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