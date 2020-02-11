import configparser
from getpass import getpass

import protocol
from chat_client.chat_client import ChatClient


class CommandlineCommander:
    def __init__(self, server_address, port):
        """

        """
        self.username = None
        self.password = None
        self.chat_client = ChatClient(server_address, port)
        self._start_session()

    def _start_session(self):
        """

        :return:
        """
        print('Welcome to the chat\nInput username and password please: \n')
        self.username = input('Username: ')
        self.chat_client.set_username(self.username)
        self.password = getpass()
        print("TODO: Hash password: {} \n".format(self.password))
        self.chat_client.create_connection()
        print("Ready to accept commands: \n")
        while True:
            current_command = input()
            self._handle_command(current_command)

    def _handle_command(self, command):
        """

        :param command:
        :return:
        """
        if protocol.COMMAND_QUIT in command:
            print('Thanks for using, bye!')
            exit(0)
        elif command.startswith(protocol.COMMAND_WHO):
            print('All online users: \n')
            print(self.chat_client.get_users())
        elif command.startswith(protocol.COMMAND_MSG):
            # Remove the @ from the command and separate the username from the message
            user, message = command.replace('@', '').split(' ', 1)
            self.chat_client.send_direct(user, message)
        else:
            print('Error: Command unknown')


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('../server_info.ini')
    commands = CommandlineCommander(config['vu']['ip'], config['vu']['port'])
