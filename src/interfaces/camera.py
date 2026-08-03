from picamera2 import Picamera2
from aiortc import VideoStreamTrack
from av import VideoFrame
import asyncio


class Camera:

    def __init__(self):

        self.picam = Picamera2()

        config = self.picam.create_video_configuration(
            main={
                "size": (1280,720),
                "format":"RGB888"
            }
        )

        self.picam.configure(config)


    def start(self):
        self.picam.start()



class CameraTrack(VideoStreamTrack):

    def __init__(self, camera):

        super().__init__()

        self.camera = camera


    async def recv(self):

        pts, time_base = await self.next_timestamp()

        frame = self.camera.picam.capture_array()

        video_frame = VideoFrame.from_ndarray(
            frame,
            format="rgb24"
        )

        video_frame.pts = pts
        video_frame.time_base = time_base

        return video_frame