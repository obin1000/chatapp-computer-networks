# Import the socket library.
import socket


class ChatClient:
    def __init__(self, server_adress, port, username):
        self.username = username
        # Create a new socket.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to another application.
        self.socket.connect((server_adress, port))

        self.send_queue = []

    def send(self, buffer):
        # Send bytes.
        num_bytes_sent = self.socket.send(buffer)
        # self.socket.sendall(buffer)

    def receive(self):
        # Receive bytes.
        buffer = self.socket.recv(2048)
        return buffer

    def __del__(self):
        # Close connection.
        self.socket.close()


if __name__ == '__main__':
    client1 = ChatClient('127.0.0.1', 22, 'obin1000')
