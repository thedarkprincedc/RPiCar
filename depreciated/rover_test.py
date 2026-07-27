import serial
import time
import json

rover = serial.Serial(
    "/dev/serial0",
    115200,
    timeout=1
)

def move(left, right):
    command = {
        "T": 1,
        "L": left,
        "R": right
    }

    rover.write(
        (json.dumps(command) + "\n").encode()
    )

    print(command)


try:
    print("Forward")

    move(0.3, 0.3)

    time.sleep(2)

    print("Stop")

    move(0, 0)


finally:
    rover.close()