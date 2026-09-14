from picamera2 import Picamera2
import cv2

class PiCamera:
    def __init__(
        self,
        width=1280,
        height=720,
        fps=30,
    ):
        self.camera = Picamera2()

        config = self.camera.create_video_configuration(
            main={
                "size": (width, height),
                "format": "RGB888",
            }
        )

        self.camera.configure(config)

        self.camera.set_controls({
            "FrameRate": fps,
        })

        self.camera.start()

    def read(self):
        frame = self.camera.capture_array()

        if frame is None:
            raise RuntimeError("Failed to read frame")

        return frame

    def close(self):
        self.camera.stop()

class OpenCVCamera:
    def __init__(
        self,
        device=0,
        width=1280,
        height=720,
        fps=30,
    ):
        self.camera = cv2.VideoCapture(device)

        if not self.camera.isOpened():
            raise RuntimeError(
                f"Camera did not open: {device}"
            )

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width,
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height,
        )

        self.camera.set(
            cv2.CAP_PROP_FPS,
            fps,
        )

    def read(self):
        ret, frame = self.camera.read()

        if not ret or frame is None:
            raise RuntimeError(
                "Failed to read frame"
            )

        # OpenCV returns BGR.
        # Convert to RGB so both camera
        # implementations return the same format.
        return cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB,
        )

    def close(self):
        self.camera.release()

def create_camera(
    backend="opencv",
    width=1280,
    height=720,
    fps=30,
    device=0,
):
    if backend == "picamera2":
        return PiCamera(
            width=width,
            height=height,
            fps=fps,
        )

    if backend == "opencv":
        return OpenCVCamera(
            device=device,
            width=width,
            height=height,
            fps=fps,
        )

    raise ValueError(
        f"Unknown camera backend: {backend}"
    )