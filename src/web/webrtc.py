import cv2

from av import VideoFrame
from aiortc import VideoStreamTrack
from .camera import Camera


class CameraTrack(VideoStreamTrack):

    def __init__(self, camera: Camera):
        super().__init__()
        self.camera = camera

    async def recv(self):
        pts, time_base = await self.next_timestamp()

        frame = self.camera.read()

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        telemetry = {
            "speed": 0,
            "battery": 0,
            "fps": 0
        }

        frame = self.draw_telemetry(frame, telemetry)

        video = VideoFrame.from_ndarray(
            frame,
            format="rgb24"
        )

        video.pts = pts
        video.time_base = time_base

        return video

    def draw_telemetry(self, frame, telemetry):
        lines = [
            f"Speed: {telemetry['speed']:.1f}%",
            f"Battery: {telemetry['battery']:.1f}V",
            f"FPS: {telemetry['fps']:.1f}",
            #f"Temp: {telemetry['temperature']:.1f}C",
        ]

        y = 30

        for line in lines:
            cv2.putText(
                frame,
                line,
                (20, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            y += 30

        return frame