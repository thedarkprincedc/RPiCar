import asyncio

from aiohttp import web
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
)
from aiortc.rtcrtpsender import RTCRtpSender

from ..webrtc import CameraTrack


routes = web.RouteTableDef()

pcs = set()


@routes.get("/")
async def index(request):
    print(request.app["templates"])
    return web.FileResponse(
        request.app["templates"] / "camera.html"
    )


@routes.post("/offer")
async def offer(request):
    data = await request.json()

    pc = RTCPeerConnection()
    pcs.add(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        if pc.connectionState in {
            "failed",
            "closed",
        }:
            pcs.discard(pc)
            await pc.close()

    await pc.setRemoteDescription(
        RTCSessionDescription(
            sdp=data["sdp"],
            type=data["type"],
        )
    )

    pc.addTrack(
        CameraTrack(
            request.app["camera"]
        )
    )

    transceiver = pc.getTransceivers()[0]

    capabilities = RTCRtpSender.getCapabilities("video")

    h264 = [
        codec
        for codec in capabilities.codecs
        if codec.mimeType == "video/H264"
    ]

    if h264:
        transceiver.setCodecPreferences(h264)

    answer = await pc.createAnswer()

    await pc.setLocalDescription(answer)

    while pc.iceGatheringState != "complete":
        await asyncio.sleep(0.1)

    return web.json_response({
        "sdp": pc.localDescription.sdp,
        "type": pc.localDescription.type,
    })