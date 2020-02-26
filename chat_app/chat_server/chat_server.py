import socket
import threading
import configparser
from time import sleep

import protocol


class ChatServer:
    MAX_NUM_CLIENTS = 64
    RECEIVE_SIZE = 1024
    SERVER_POLL_INTERVAL = 0.1
    CLIENT_POLL_INTERVAL = 0.1

    def __init__(self, host_address, port, socket_family=socket.AF_INET, socket_type=socket.SOCK_STREAM):
        print('Chat server is starting on {}:{}'.format(host_address, port))
        self.port = port
        self.host_address = host_address
        # Used to stop all threads
        self.alive = True
        # Store all client threads
        self.clients = {}

        self.socket = socket.socket(socket_family, socket_type)
        # Bind to all interfaces of the server on given port
        self.socket.bind(('', port))
        # become a server socket
        self.socket.listen(self.MAX_NUM_CLIENTS)

    def start_polling(self):
        username = 'moi'
        while True:
            # accept connections from outside
            (client_socket, address) = self.socket.accept()
            if client_socket:
                # Create a client for each connection
                self.create_client(username, client_socket)
                sleep(self.SERVER_POLL_INTERVAL)
            else:
                print('Server accepted an empty connection!')

    def create_client(self, username, client_connection):
        client_thread = threading.Thread(target=self._client_poll, args=client_connection)
        self.clients[username] = client_thread
        client_thread.start()

    def remove_client(self, username):
        self.clients.pop(username)

    def _client_poll(self, client):
        message = ''
        while self.alive:
            data = client.recv(self.RECEIVE_SIZE)
            message += data.decode()

            # For messages lager than the buffer, search for the message end.
            if protocol.MESSAGE_END not in message:
                continue

            self._handle_request(client, message)

            # Reset message for next message
            message = ''

            sleep(self.CLIENT_POLL_INTERVAL)

    def _handle_request(self, client, message):
        client.sendall(message)

    def _handle_message(self):
        pass

    def __del__(self):
        self.alive = False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../../server_info.ini')
    server = ChatServer(config['DEFAULT']['ip'], config['DEFAULT']['port'])
