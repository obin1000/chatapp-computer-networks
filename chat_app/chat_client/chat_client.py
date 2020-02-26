# Import the socket library.
import os
import socket
import threading
import configparser
import protocol
from time import sleep


class ChatClient:
    MAX_MSG_LENGTH = 10
    RECEIVE_SIZE = 1024
    RECEIVE_INTERVAL = 0.1
    SEND_INTERVAL = 0.5

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
        self.sending = False
        self.sending_thread = None

        # Thread that polls for new messages
        self.polling_thread = None
        # Indicates if the client should be polling
        self.polling = False

    def create_connection(self, socket_family=socket.AF_INET, socket_type=socket.SOCK_STREAM):
        """
        Create the socket connection between this client en given server in the constructor.
        :param socket_family: Protocol to be used by sockets, defaults to INET (IP).
        :param socket_type: Packaging  type to be used by sockets, defaults to STREAM.
        :return: True if connection was successful, else false.
        """
        try:
            # Create a new socket.
            self.socket = socket.socket(socket_family, socket_type)
            # Connect to another application.
            self.socket.connect((self.server_address, self.port))
            return True
        except:
            print('Failed connecting to {}:{}'.format(self.server_address, self.port))
            return False

    def do_handshake(self, username):
        """
        Do the handshake provided from our protocol
        :param username: Name of the user to represent yourself at the server.
        :return: Tuple. True if successful, False if failed. Followed by reason string.
        """
        buffer = str.encode("{} {}{}".format(protocol.HELLO_FROM, username, protocol.MESSAGE_END))
        num_bytes_sent = self.socket.sendall(buffer)
        response = self.socket.recv(self.RECEIVE_SIZE)
        decoded = response.decode()
        return self._check_response(decoded)

    def start_polling(self):
        """
        Creates a thread to start polling form incoming messages. Only 1 can be active at a time
        :return:
        """
        if self.polling_thread is None:
            self.polling_thread = threading.Thread(target=self._poll)
            self.polling_thread.start()
        else:
            print('Polling already active!')

    def stop_polling(self):
        """
        Stops the polling thread if it is polling.
        :return: None
        """
        self.polling = False

    def _poll(self):
        """
        Poll for incoming messages.
        :return:
        """
        message = ''
        self.polling = True
        while self.polling:
            received = self.socket.recv(self.RECEIVE_SIZE)
            message += received.decode()

            # For messages lager than the buffer, search for the message end.
            if protocol.MESSAGE_END not in message:
                continue

            # Only report bad responses and deliveries to the user
            good, reason = self._check_response(message)
            if not good:
                print('Bad response: ' + reason)
            elif protocol.DELIVERY in message:
                user, msg = message.replace(protocol.DELIVERY, '', 1).replace(' ', '', 1).split(' ', 1)
                print('{}: {}'.format(user, msg))
            elif protocol.WHO_OK in message:
                users = message.replace(protocol.WHO_OK, '', 1).replace(' ', '', 1)
                print('{}'.format(users))

            message = ''
            sleep(self.RECEIVE_INTERVAL)

    def _check_response(self, message):
        """
        Check a received message from the server.
        :param message: The message to be checked.
        :return: Tuple. True if successful, False if failed. Followed by reason string.
        """
        if message is None:
            return False
        else:
            for good in protocol.GOOD_RESPONSE:
                if good in message:
                    return True, good

            for bad in protocol.BAD_RESPONSE:
                if bad in message:
                    return False, bad

    def get_users(self):
        """
        Get current only users.
        :return: A string listing all online users.
        """
        buffer = '{}{}'.format(protocol.WHO, protocol.MESSAGE_END)
        self.send(buffer)

    def start_sending(self):
        """

        :return:
        """
        if self.sending_thread is None:
            self.sending_thread = threading.Thread(target=self._sending)
            self.sending_thread.start()
        else:
            print('Sending already active!')

    def stop_sending(self):
        """

        :return:
        """
        self.sending = False

    def _sending(self):
        """

        :return:
        """
        self.sending = True
        while self.sending:
            if self.send_queue:
                message = self.send_queue.pop(0)
                # Encode string to bytes and send
                self.socket.sendall(str.encode(message))

            sleep(self.SEND_INTERVAL)

    def send(self, message):
        """
        Add message to send queue
        :return:
        """
        self.send_queue.append(message)

    def send_message(self, user, message):
        """
        Send a message to another user.
        :param user: The user to send the message to.
        :param message: The message to send
        :return: None
        """
        buffer = "{} {} {}{}".format(protocol.SEND, user, message, protocol.MESSAGE_END)
        self.send(buffer)

    def stop(self):
        """
        Stops
        :return:
        """
        self.__del__()

    def __del__(self):
        """
        Cleanup after destroying this object. Close connection.
        :return: None
        """
        self.socket.close()
        self.polling = False
        if self.polling_thread:
            self.polling_thread = None
        os._exit(0)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../../server_info.ini')
    client1 = ChatClient(config['DEFAULT']['ip'], config['DEFAULT']['port'])
