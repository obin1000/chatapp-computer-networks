from chat_client.chat_client import ChatClient
import socket


class UDPChatClient(ChatClient):

    def create_connection(self, socket_family=socket.AF_INET, socket_type=socket.SOCK_DGRAM):
        """
        This overrides the TCP connection with an UDP connection.
        :param socket_family:
        :param socket_type:
        :return:
        """
        super().create_connection(socket_family=socket.AF_INET, socket_type=socket.SOCK_DGRAM)
