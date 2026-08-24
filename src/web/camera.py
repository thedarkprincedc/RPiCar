import cv2

class Camera:
    def __init__(
        self, 
        device=0, 
        width=1920, 
        height=1080, 
        fps=60
    ):
        self.camera = cv2.VideoCapture(
            device, 
            cv2.CAP_DSHOW
        )
        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height
        )

        self.camera.set(
            cv2.CAP_PROP_FPS,
            fps
        )

        if not self.camera.isOpened():
            raise RuntimeError("Camera did not open")

    def read(self):
        success, frame = self.camera.read()

        if not success:
            raise RuntimeError("Failed to read frame")

        return frame

    def close(self):
        self.camera.release()