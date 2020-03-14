import configparser
from time import sleep
from getpass import getpass

import protocol
from chat_client.chat_client import ChatClient
from chat_client.udp_chat_client import UDPChatClient


class CommandlineCommander:
    SOCKET_CREATE_INTERVAL = 0.5
    CLIENT_UDP = 2
    CLIENT_TCP = 1

    def __init__(self, server_address, port, client_type=CLIENT_TCP):
        """
        Creates a chat client and starts a commandline session.
        """
        self.username = None
        self.password = None
        if client_type is self.CLIENT_TCP:
            self.chat_client = ChatClient(server_address, port)

        elif client_type is self.CLIENT_UDP:
            self.chat_client = UDPChatClient(server_address, port)
        else:
            print('Client got invalid client type: {}. Cannot continue'.format(client_type))
        self._start_session()

    def _start_session(self):
        """
        Setup a chat client and grab user input.
        :return: None
        """
        print('Input username and password please: \n')

        self.chat_client.start_polling()
        self.chat_client.start_sending()

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

            self.chat_client.do_handshake(self.username)

        # self.password = getpass()
        # print("TODO: Hash password: {} \n".format(self.password))

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
    commands = CommandlineCommander(config['DEFAULT']['ip'], config['DEFAULT']['port'])
