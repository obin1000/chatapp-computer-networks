import configparser
from chat_client.commandline_commander import CommandlineCommander
from chat_server.chat_server import ChatServer
import sys

config = configparser.ConfigParser()
config.read('server_info.ini')
if len(sys.argv) < 2:
    print('No arguments found, please try running this with --client or --server')

for arg in sys.argv:
    if 'chat_app' in arg:
        print('Welcome to the chat')
    elif '--server' in arg:
        server = ChatServer(config['DEFAULT']['ip'], config['DEFAULT']['port'])
    elif '--client' in arg:
        commandline = CommandlineCommander(config['DEFAULT']['ip'], config['DEFAULT']['port'])
    elif '--udp-client' in arg:
        server = CommandlineCommander(config['DEFAULT']['ip'], config['DEFAULT']['port'],
                                      CommandlineCommander.CLIENT_UDP)
    elif '--udp-server' in arg:
        pass
    else:
        print('Could not understand argument {}'.format(arg))
