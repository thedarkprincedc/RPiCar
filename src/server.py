from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# route endpoints
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
   return render_template("video.html")

@app.route("/controls")
def controls():
   return render_template("controls.html")

@app.route("/status")
def status():
   return render_template("status.html")

# socket endpoints
@socketio.on("connect")
def on_connect():
    print(f"Connected: {request.sid}")

@socketio.on("disconnect")
def on_disconnect():
    print(f"Disconnected: {request.sid}")

@socketio.on("message")
def handle_message(data):
    print("From:", request.sid)
    print("Data:", data)

if __name__ == "__main__":
    #app.run(debug=True)
    socketio.run(app, host="0.0.0.0", port=3000, debug=True)