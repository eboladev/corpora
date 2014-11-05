import config
import Queue
import socket
import threading
import trace

class MessagingAgent(threading.Thread):

    def __init__(self, id, conn, host, port):
        super(MessagingAgent, self).__init__()
        self.daemon = True
        self.name = 'messaging-{}'.format(id)
        self.queue = Queue.Queue()
        self.socket = conn
        self.host = host
        self.port = port

        conn.settimeout(config.MESSAGING_WAIT_INTERVAL)

    def run(self):
        trace.info('Accepted client from {}:{}'.format(self.host, self.port))

        while True:
            try:
                response = self.queue.get_nowait()
            except Queue.Empty: pass

            try:
                data = self.socket.recv(config.MESSAGING_BUFFER_SIZE)
                if not data:
                    break   # Connection closed
                else:
                    trace.info('Received', str(data).strip())
            except socket.timeout: pass

        self.socket.close()
        trace.info('Client {}:{} closed'.format(self.host, self.port))
