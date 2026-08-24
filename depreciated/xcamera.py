from flask import Flask, Response
from picamera2 import Picamera2
import cv2
import time

app = Flask(__name__)

# Initialize camera
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"size": (1280, 720), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

# Give the camera a moment to warm up
time.sleep(2)


def generate():
    while True:
        frame = picam2.capture_array()

        success, buffer = cv2.imencode(".jpg", frame)
        if not success:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )


@app.route("/")
def index():
    return """
    <html>
        <head>
            <title>Pi Camera Test</title>
        </head>
        <body>
            <h2>Raspberry Pi Camera</h2>
            <img src="/stream" width="960">
        </body>
    </html>
    """


@app.route("/stream")
def stream():
    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)