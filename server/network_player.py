from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('connect')
def network_connect():
    print("client has connected")

@socketio.on('disconnect')
def network_disconnect():
    print("client has disconnected")

@socketio.on('update')
def client_update(controller_state):
    print(controller_state)

if __name__ == '__main__':
    socketio.run(app, "0.0.0.0", port=5000)
    pass
