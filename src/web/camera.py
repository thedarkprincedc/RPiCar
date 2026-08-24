import cv2
import platform

class Camera:
    def __init__(
        self, 
        device=0, 
        width=1920, 
        height=1080, 
        fps=60
    ):
        platform_os = platform.system()
        capture_os = {
            'Windows': cv2.CAP_MSMF,
            'Linux': cv2.CAP_V4L2
        }

        if(capture_os[platform_os] == None):
            raise Exception("No capture format found for os")
        
        self.camera = cv2.VideoCapture(
            device, 
            capture_os[platform_os]
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