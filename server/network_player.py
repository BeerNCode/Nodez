from flask import Flask, request
from flask_socketio import SocketIO
import threading
import json
import logging

logger = logging.getLogger(__name__)
app = Flask(__name__)
socketio = SocketIO(app)
players = {}

@socketio.on('connect')
def network_connect():
    client_id = request.sid
    logger.debug(f"client [{client_id}] has connected")
    players[client_id] = {"state": {"up": None, "down": None, "left": None, "right": None, "a": None}}

@socketio.on('disconnect')
def network_disconnect():
    client_id = request.sid
    logger.debug(f"client [{client_id}] has disconnected")
    del players[client_id]

@socketio.on('update')
def client_update(controller_state):
    client_id = request.sid
    players[client_id]["state"] = controller_state
 
def run_thread():
    thread = threading.Thread(target=run)
    thread.start()

def run():
    socketio.run(app, "0.0.0.0", port=5000)