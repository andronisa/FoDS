__author__ = 'Adisorn'

import tornado.websocket

class LogBroadcaster(object):

    def __init__(self):
        super(LogBroadcaster, self).__init__()
        self.__subscribers = []

    def add_subscriber(self, web_socket):
        self.__subscribers.append(web_socket)

    def remove_subscriber(self, web_socket):
        self.__subscribers.remove(web_socket)

    def broadcast_message(self, message):
        for web_socket in self.subscribers:
            web_socket.write_message(message)

    @property
    def subscribers(self):
        return self.__subscribers

