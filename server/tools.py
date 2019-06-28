import logging
import json
    
logger = logging.getLogger(__name__)
BUFFER_SIZE = 4096

def read_json(socket):
    try:       
        data = socket.recv(BUFFER_SIZE)
        logger.debug(data)

        if not data is None:
            return json.JSONDecoder().decode(data.decode('utf-8'))
        return None
    except Exception as e:
        logger.error("Unable to receive json data.")
        logger.debug(e.args)