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

        video = VideoFrame.from_ndarray(
            frame,
            format="rgb24"
        )

        video.pts = pts
        video.time_base = time_base

        return video