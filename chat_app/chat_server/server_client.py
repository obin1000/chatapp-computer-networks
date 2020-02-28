import threading
from time import sleep
import protocol


class ServerClient:
    CLIENT_POLL_INTERVAL = 0.1
    RECEIVE_SIZE = 1024

    def __init__(self, client_connection, user_id=None, username=None):
        print('Created user')
        self.client_connection = client_connection
        self.user_id = user_id
        self.username = username
        self.done_handshake = False
        self.poll_thread = None
        # Variable to stop the poll threads
        self.alive = True

        self.send_box = []

        self.start_polling()

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_user_id(self):
        return self.user_id

    def get_send_item(self):
        return self.send_box.pop(0)

    def start_polling(self):
        self.poll_thread = threading.Thread(target=self._client_poll)
        self.poll_thread.start()

    def _client_poll(self):
        message = ''
        while self.alive:
            data = self.client_connection.recv(self.RECEIVE_SIZE)
            message += data.decode()

            # For messages lager than the buffer, search for the message end.
            if protocol.MESSAGE_END not in message:
                continue

            print('Received {} from {}'.format(message, self.user_id))

            self.send_box.append(message)

            # Reset message for next message
            message = ''

            sleep(self.CLIENT_POLL_INTERVAL)

    def send(self, message):
        self.client_connection.sendall()

    def __del__(self):
        del self.poll_thread
