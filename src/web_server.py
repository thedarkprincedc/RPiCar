from flask import Flask, render_template
from flask_socketio import SocketIO

class WebServer:
    def __init__(self, state):
        self.state = state

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        self.register_routes()
        self.register_events()

    def register_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

    def register_events(self):
        @self.socketio.on("connect")
        def connect():
            print("Client connected")
            self.socketio.emit("state", self.state.snapshot())

        @self.socketio.on("disconnect")
        def disconnect():
            print("Client disconnected")

    def send_state(self):
        self.socketio.emit("state", self.state.snapshot())

    def run(self):
        self.socketio.run(self.app, 
            host="0.0.0.0", 
            port=3000, 
            debug=False,
            use_reloader=False
        )