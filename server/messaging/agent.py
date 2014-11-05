import threading
import trace

class MessagingAgent(threading.Thread):

    def __init__(self, id, conn, host, port):
        super(MessagingAgent, self).__init__()
        self.daemon = True
        self.name = 'messaging-{}'.format(id)
        self.socket = conn
        self.host = host
        self.port = port

    def run(self):
        trace.info('Accepted client from {}:{}'.format(self.host, self.port))
