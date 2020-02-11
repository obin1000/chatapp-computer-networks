# Import the socket library.
import socket
import threading
import configparser
import protocol
from time import sleep


class ChatClient:
    MAX_MSG_LENGTH = 10
    RECEIVE_SIZE = 2048
    RECEIVE_INTERVAL = 0.1

    def __init__(self, server_address, port):
        """
        Start a connection to the chat server.
        :param server_address: IP of the server.
        :param port: Port of the server application.
        """
        self.server_address = server_address
        self.port = int(port)
        self.socket = None
        self.username = 'Loser'
        # Queue for message to send to the server
        self.send_queue = []
        self.listen_thread = None

    def set_username(self, username):
        self.username = username

    def create_connection(self, socket_family=socket.AF_INET, socket_type=socket.SOCK_STREAM):
        # Create a new socket.
        self.socket = socket.socket(socket_family, socket_type)
        # Connect to another application.
        self.socket.connect((self.server_address, self.port))
        self._handshake()
        self._start_listening()

    def _handshake(self):
        buffer = str.encode("{} {}{}".format(protocol.HELLO_FROM, self.username, protocol.MESSAGE_END))
        num_bytes_sent = self.socket.sendall(buffer)

    def _start_listening(self):
        if self.listen_thread is None:
            self.listen_thread = threading.Thread(target=self._listener)
            self.listen_thread.start()

    def _listener(self):
        while True:
            received = self.socket.recv(self.RECEIVE_SIZE)
            print(received)
            sleep(self.RECEIVE_INTERVAL)

    def get_users(self):
        # Encode string to bytes
        buffer = str.encode(protocol.WHO + protocol.MESSAGE_END)
        num_bytes_sent = self.socket.sendall(buffer)

    def start_sync(self):
        """
        Start syncing this client with the server.
        :return:
        """
        buffer = self.send_queue.pop(0)
        num_bytes_sent = self.socket.sendall(buffer)

    def check_response(self, response):
        pass

    def send(self, user, message):
        """
        Add a message to the send queue.
        :param buffer:
        :return:
        """
        self.send_queue.append(message)

    def send_direct(self, user, message):
        """

        :param buffer:
        :return:
        """
        buffer = str.encode("{} {} {}{}".format(protocol.SEND, user, message, protocol.MESSAGE_END))
        num_bytes_sent = self.socket.sendall(buffer)

    def __del__(self):
        # Close connection.
        self.socket.close()
        self.listen_thread = None


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../../server_info.ini')
    client1 = ChatClient(config['vu']['ip'], config['vu']['port'])
