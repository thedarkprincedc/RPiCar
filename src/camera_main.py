from interfaces.camera import Camera
from web.app import WebServer


camera = Camera()

camera.start()


server = WebServer(
    camera
)


server.app.run(
    host="0.0.0.0",
    port=3000
)