import configparser
from time import sleep
from getpass import getpass

import protocol
from chat_client.chat_client import ChatClient


class CommandlineCommander:
    SOCKET_CREATE_INTERVAL = 0.5
    def __init__(self, server_address, port):
        """
        Creates a chat client and starts a commandline session.
        """
        self.username = None
        self.password = None
        self.chat_client = ChatClient(server_address, port)
        self._start_session()

    def _start_session(self):
        """
        Setup a chat client and grab user input.
        :return: None
        """
        print('Input username and password please: \n')
        # Loop until a good username is found
        successful = False
        while not successful:
            # Server breaks connection after bad handshake
            if not self.chat_client.create_connection():
                sleep(self.SOCKET_CREATE_INTERVAL)
                continue

            self.username = input('Username: ')

            if not self._check_username(self.username):
                print('Username {} is invalid'.format(self.username))
                continue

            successful, reason = self.chat_client.do_handshake(self.username)
            print('Username was {}: {}'.format(successful, reason))

        # self.password = getpass()
        # print("TODO: Hash password: {} \n".format(self.password))

        self.chat_client.start_polling()
        self.chat_client.start_sending()

        print("Ready to accept commands: \n")
        while True:
            current_command = input()
            self._handle_command(current_command)

    def _check_username(self, username):
        """
        Checks if given username is valid.
        :param username: Username to check.
        :return: True if given username is valid, else False.
        """
        # Username cannot contain spaces
        if ' ' in username:
            return False
        else:
            return True

    def _handle_command(self, command):
        """
        Convert a command from the input to action in the chat client.
        :param command: Command to check.
        :return: None
        """
        if protocol.COMMAND_QUIT in command:
            print('Thanks for using, bye!')
            self.__del__()
            exit(0)
        elif command.startswith(protocol.COMMAND_WHO):
            print('All online users: \n')
            self.chat_client.get_users()
        elif command.startswith(protocol.COMMAND_MSG):
            # Remove the @ from the command and separate the username from the message
            user, message = command.replace('@', '', 1).split(' ', 1)
            self.chat_client.send_message(user, message)
        else:
            print('Error: Command unknown')

    def __del__(self):
        """
        Cleanup
        :return: None
        """
        self.chat_client.stop()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../server_info.ini')
    commands = CommandlineCommander(config['vu']['ip'], config['vu']['port'])
