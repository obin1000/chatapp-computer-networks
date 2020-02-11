import configparser
from commandline_commander import CommandlineCommander

config = configparser.ConfigParser()
config.read('server_info.ini')
commandline = CommandlineCommander(config['vu']['ip'], config['vu']['port'])