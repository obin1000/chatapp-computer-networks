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
        # Queue for message to send to the server
        self.send_queue = []
        # Thread that polls for new messages
        self.polling_thread = None
        # Indicates if the client should be polling
        self.polling = False

    def create_connection(self, socket_family=socket.AF_INET, socket_type=socket.SOCK_STREAM):
        """
        Create the socket connection between this client en given server in the constructor.
        :param socket_family: Protocol to be used by sockets, defaults to INET (IP).
        :param socket_type: Packaging  type to be used by sockets, defaults to STREAM.
        :return: None
        """
        # Create a new socket.
        self.socket = socket.socket(socket_family, socket_type)
        # Connect to another application.
        self.socket.connect((self.server_address, self.port))

    def do_handshake(self, username):
        """
        Do the handshake provided from our protocol
        :param username: Name of the user to represent yourself at the server.
        :return: True if successful, False if failed.
        """
        buffer = str.encode("{} {}{}".format(protocol.HELLO_FROM, username, protocol.MESSAGE_END))
        num_bytes_sent = self.socket.sendall(buffer)
        response = self.socket.recv(self.RECEIVE_SIZE)

        if protocol.IN_USE in response.decode():
            return False, protocol.IN_USE
        else:
            return True, 'Success'

    def start_polling(self):
        """
        Creates a thread to start polling form incoming messages. Only 1 can be active at a time
        :return:
        """
        if self.polling_thread is None:
            self.polling_thread = threading.Thread(target=self._poll)
            self.polling_thread.start()

    def stop_polling(self):
        """
        Stops the polling thread if it is polling.
        :return: None
        """
        self.polling = False

    def _poll(self):
        """
        Poll for incoming messages
        :return:
        """
        self.polling = True
        while self.polling:
            received = self.socket.recv(self.RECEIVE_SIZE)
            self._check_response(received.decode())
            sleep(self.RECEIVE_INTERVAL)

    def _check_response(self, message):
        """
        Check a received message from the server.
        :param message: The message to be checked.
        :return: None
        """
        if protocol.DELIVERY in message:
            user, msg = message.replace(protocol.DELIVERY, '', 1).replace(' ', '', 1).split(' ', 1)
            print('{}: {}'.format(user, msg))
        else:
            print(message)

    def get_users(self):
        """
        Get current only users.
        :return: A string listing all online users.
        """
        # Encode string to bytes
        buffer = str.encode(protocol.WHO + protocol.MESSAGE_END)
        num_bytes_sent = self.socket.sendall(buffer)

    def send_direct(self, user, message):
        """
        Send a message to another user.
        :param user: The user to send the message to.
        :param message: The message to send
        :return: None
        """
        buffer = str.encode("{} {} {}{}".format(protocol.SEND, user, message, protocol.MESSAGE_END))
        num_bytes_sent = self.socket.sendall(buffer)

    def __del__(self):
        """
        Cleanup after destroying this object.
        :return: None
        """
        # Close connection.
        self.socket.close()
        if self.polling_thread is not None:
            self.polling = False
            self.polling_thread = None


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../../server_info.ini')
    client1 = ChatClient(config['vu']['ip'], config['vu']['port'])
