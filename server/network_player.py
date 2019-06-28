    # def listen_for_new_clients(self):
    #     self.socket.bind((IP_ADDRESS, PORT))
    #     self.socket.listen(5)
    #     self.socket.settimeout(CLIENT_TIMEOUT)
    #     while self.running:
    #         try:
    #             logger.info(f"Listening for connection....")
    #             connection, ip_address = self.socket.accept()
    #             logger.info(f"Received connection from [{ip_address}]")
    #             client = clients.Client(connection, ip_address)
    #             client.connection.settimeout(CLIENT_TIMEOUT)
    #             client.start_listening()
    #             self.clients.append(client)

    #         except Exception as e:
    #             logger.error("Unable to connect to client.")
    #             logger.debug(e.args)

    # class Client():
    # def __init__(self, connection, ip_address):
    #     self.connection = connection
    #     self.ip_address = ip_address
    #     self.running = True
    #     self.keys = {}
    #     self.listen_thread = threading.Thread(target=self.listen)

    # def start_listening(self):
    #     self.listen_thread.start()

    # def listen(self):
    #     logger.info("Listening to client.")
    #     while self.running:
    #         data = read_json(self.connection)
    #         if data is not None:
    #             self.keys = data