import config
import socket
from base import BaseService

class MessagingService(BaseService):

    def __init__(self):
        super(MessagingService, self).__init__('messaging')

        s = socket.socket()
        s.bind((config.MESSAGING_HOST, config.MESSAGING_PORT))
        s.listen(config.MESSAGING_MAX_PENDING_CLIENTS)
        self.socket = s

    def wait(self):
        return self.socket.accept()

    def handle(self, conn, addr):
        (host, port) = addr
        print('Connected to %s:%s' % addr)
        conn.close()
