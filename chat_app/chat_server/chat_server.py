import socket
import threading
import configparser
from time import sleep

import protocol
from chat_server.server_client import ServerClient


class ChatServer:
    MAX_NUM_CLIENTS = 64
    SERVER_POLL_INTERVAL = 0.1

    def __init__(self, host_address, port, socket_family=socket.AF_INET, socket_type=socket.SOCK_STREAM):
        print('Chat server is starting on {}:{}'.format(host_address, port))
        self.port = port
        self.host_address = host_address
        # Used to stop all threads
        self.alive = True
        # Store all client threads
        self.clients = []

        self.connection_poll_thread = None

        self.socket = socket.socket(socket_family, socket_type)
        # Bind to all interfaces of the server on given port
        self.socket.bind(('', int(port)))
        # become a server socket, plus 1 connection so we can close the connection in _ connection_polling
        self.socket.listen(self.MAX_NUM_CLIENTS + 1)
        self.start_connection_polling()

    def start_connection_polling(self):
        self.connection_poll_thread = threading.Thread(target=self._connection_poll)
        self.connection_poll_thread.start()

    def _connection_poll(self):
        while True:
            # accept connections from outside
            (client_socket, address) = self.socket.accept()
            if len(self.clients) >= self.MAX_NUM_CLIENTS:
                print('Server has reached max users!')
                client_socket.sendall(str.encode(protocol.BUSY + protocol.MESSAGE_END))
                client_socket.close()

            if client_socket:
                # Create a client for each connection
                self.create_client(client_socket)
            else:
                print('Server accepted an empty connection!')

            sleep(self.SERVER_POLL_INTERVAL)

    def start_client_polling(self):
        self.connection_poll_thread = threading.Thread(target=self._client_poll)

    def _client_poll(self):
        for client in self.clients:
            pass

    def create_client(self, client_connection):
        new_client = ServerClient(client_connection)
        self.clients.append(new_client)
        new_client.set_user_id(len(self.clients) - 1)

    def check_username(self, username):
        for client in self.clients:
            if username is client.get_username():
                return False

        return True

    def remove_client(self, username):
        client = self.clients.pop(username.get_user_id())
        if client:
            client.close()

    def __del__(self):
        self.alive = False


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../../server_info.ini')
    server = ChatServer(config['DEFAULT']['ip'], config['DEFAULT']['port'])
