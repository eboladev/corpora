import config
import trace
import socket
from base import BaseService

class MessagingService(BaseService):

    def __init__(self):
        super(MessagingService, self).__init__('messaging')

        s = socket.socket()
        s.bind((config.MESSAGING_HOST, config.MESSAGING_PORT))
        s.listen(config.MESSAGING_MAX_PENDING_CLIENTS)
        self.socket = s

        trace.info('Listening on port', config.MESSAGING_PORT)

    def wait(self):
        return self.socket.accept()

    def handle(self, conn, addr):
        (host, port) = addr
        trace.info('Client', host, ':', port, 'connected')
        conn.sendall('Hello world!\n')
        conn.close()
