from flask import Flask, request, jsonify, render_template
from aiortc import RTCPeerConnection, RTCSessionDescription

from cam.camera import CameraTrack


pcs = set()


class WebServer:


    def __init__(self, camera):

        self.camera = camera

        self.app = Flask(
            __name__,
            template_folder="templates"
        )


        self.setup_routes()



    def setup_routes(self):


        @self.app.route("/")
        def index():

            return render_template(
                "index.html"
            )



        @self.app.route(
            "/offer",
            methods=["POST"]
        )
        async def offer():

            data = request.json


            pc = RTCPeerConnection()

            pcs.add(pc)


            await pc.setRemoteDescription(
                RTCSessionDescription(
                    sdp=data["sdp"],
                    type=data["type"]
                )
            )


            pc.addTrack(
                CameraTrack(
                    self.camera
                )
            )


            answer = await pc.createAnswer()

            await pc.setLocalDescription(
                answer
            )


            return jsonify(
                {
                    "sdp": pc.localDescription.sdp,
                    "type": pc.localDescription.type
                }
            )