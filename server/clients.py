import logging
import json
import threading
from tools import *

logger = logging.getLogger(__name__)

class Client():
    def __init__(self, connection, ip_address):
        self.connection = connection
        self.ip_address = ip_address
        self.running = True
        self.keys = {}
        self.listen_thread = threading.Thread(target=self.listen)

    def start_listening(self):
        self.listen_thread.start()

    def listen(self):
        logger.info("Listening to client.")
        while self.running:
            data = read_json(self.connection)
            if data is not None:
                self.keys = data