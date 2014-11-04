import config
import socket
from base import BaseService

class MessagingService(BaseService):

    def __init__(self):
        super.__init__(self, 'messaging')

        s = socket.socket()
        s.bind((config.MESSAGING_HOST, config.MESSAGING_PORT))
        s.listen(config.MESSAGING_MAX_PENDING_CLIENTS)
        self.socket = s

    def run(self):
        pass
