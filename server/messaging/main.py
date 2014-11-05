import config
import trace
import socket
from agent import MessagingAgent
from base import BaseService
from threading import Lock

class MessagingService(BaseService):

    def __init__(self):
        super(MessagingService, self).__init__('messaging')

        self.counter = 0
        self.clients = []
        self.users = {}
        self.channels = {}
        self.lock = Lock()

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((config.MESSAGING_HOST, config.MESSAGING_PORT))
        s.listen(config.MESSAGING_MAX_PENDING_CLIENTS)
        self.socket = s

        trace.info('Listening on port', config.MESSAGING_PORT)

    def wait(self):
        return self.socket.accept()

    def handle(self, conn, addr):
        (host, port) = addr
        self.counter += 1

        agent = MessagingAgent(self, self.counter, conn, host, port)
        self.clients.append(agent)
        agent.start()
