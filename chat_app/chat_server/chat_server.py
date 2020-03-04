import socket
import threading
import configparser
from time import sleep

import protocol
from chat_server.server_client import ServerClient


class ChatServer:
    MAX_NUM_CLIENTS = 64
    SERVER_CONNECTION_POLL_INTERVAL = 0.1
    SERVER_CLIENT_POLL_INTERVAL = 0.2

    def __init__(self, host_address, port, socket_family=socket.AF_INET, socket_type=socket.SOCK_STREAM):
        print('Chat server is starting on {}:{}'.format(host_address, port))
        self.port = port
        self.host_address = host_address
        # Used to stop all threads
        self.alive = True
        # Store all client threads in an array
        self.clients = []

        self.connection_poll_thread = None

        self.socket = socket.socket(socket_family, socket_type)
        # Bind to all interfaces of the server on given port
        self.socket.bind(('', int(port)))
        # become a server socket, plus 1 connection so we can close the connection in _ connection_polling
        self.socket.listen(self.MAX_NUM_CLIENTS + 1)
        self.start_connection_polling()
        self.start_client_polling()

    def start_connection_polling(self):
        self.connection_poll_thread = threading.Thread(target=self._connection_poll)
        self.connection_poll_thread.start()

    def _connection_poll(self):

        while self.alive:
            # accept connections from outside
            try:
                (client_socket, address) = self.socket.accept()

                if len(self.clients) >= self.MAX_NUM_CLIENTS:
                    print('Server has reached max users!')
                    client_socket.sendall(str.encode(protocol.BUSY + protocol.MESSAGE_END))
                    client_socket.close()

                if client_socket:
                    # Create a client for each connection
                    self.create_client(client_socket, address)
                else:
                    print('Server accepted an empty connection!')
            except Exception as e:
                print('Client connection error: {}'.format(e))

            sleep(self.SERVER_CONNECTION_POLL_INTERVAL)

    def start_client_polling(self):
        self.connection_poll_thread = threading.Thread(target=self._client_poll)
        self.connection_poll_thread.start()

    def _client_poll(self):
        while self.alive:
            sleep(self.SERVER_CLIENT_POLL_INTERVAL)
            if self.clients:
                for client in self.clients:
                    if client.is_alive():
                        message = client.get_next_message()
                        if message:
                            self.handle_request(message, client)
                    else:
                        self.remove_client(client)

    def create_client(self, client_connection, address):
        full_address = '{}:{}'.format(address[0], address[1])
        new_client = ServerClient(client_connection, address=full_address)
        self.clients.append(new_client)

    def check_username(self, username):
        for client in self.clients:
            if username == client.get_username():
                return False

        return True

    def get_current_clients(self):
        clients_listed = ' '
        for client in self.clients:
            username = client.get_username()
            if username:
                clients_listed += username + ','

        return clients_listed

    def get_client_by_username(self, username):
        """
        Get a ServerClient object bases on username.
        :param username: Username of the client
        :return: ServerClient object of the username
        """
        for client in self.clients:
            if client.get_username() == username:
                return client

        return None

    def handle_request(self, request, client):
        if request.startswith(protocol.HELLO_FROM) and not client.get_handshake_done():
            username = request.replace(protocol.MESSAGE_END, '').split(' ')[1]
            if self.check_username(username):
                client.set_username(username)
                client.handshake_done()
                client.send('{} {}{}'.format(protocol.HELLO, username, protocol.MESSAGE_END))
            else:
                client.send('{}{}'.format(protocol.IN_USE, protocol.MESSAGE_END))
                self.remove_client(client)

        elif request.startswith(protocol.WHO):
            client.send('{} {}{}'.format(protocol.WHO_OK, self.get_current_clients(), protocol.MESSAGE_END))

        elif request.startswith(protocol.SEND):
            target_username, message = request.replace(protocol.SEND, '', 1).replace(protocol.MESSAGE_END, '')\
                .replace(' ', '', 1).split(' ', 1)
            print(target_username)
            target_user = self.get_client_by_username(target_username)

            if target_user is None:
                client.send('{}{}'.format(protocol.UNKNOWN, protocol.MESSAGE_END))
                return 1

            target_user.send('{} {} {}{}'.format(protocol.DELIVERY, client.get_username(),
                                                 message, protocol.MESSAGE_END))

            client.send('{}{}'.format(protocol.SEND_OK, protocol.MESSAGE_END))

        else:
            client.send('{}{}'.format(protocol.BAD_RQST_HDR, protocol.MESSAGE_END))

    def remove_client(self, client):
        print('Removing {}'.format(client.get_username()))
        try:
            client.kill()
            self.clients.remove(client)
            del client
        except ValueError as e:
            print('Tried removing non existing user')

    def __del__(self):
        if self.alive:
            self.alive = False

        for client in self.clients:
            del client

        if self.socket:
            self.socket.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../../server_info.ini')
    server = ChatServer(config['DEFAULT']['ip'], config['DEFAULT']['port'])
