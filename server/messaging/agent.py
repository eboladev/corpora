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

        buf, request = '', ''
        response = None

        while True:
            try:
                response = self.queue.get_nowait()
            except Queue.Empty: pass

            if response:
                trace.info('Response', response)
                pass

            try:
                data = self.socket.recv(config.MESSAGING_BUFFER_SIZE)

                if data:
                    buf += data
                    end = buf.find('\n\n')
                    if end >= 0:
                        request = buf[:end]
                        buf = buf[end + 2:]
                else:
                    break   # Connection closed
            except socket.timeout: pass

            if request:
                trace.info('Request', request.strip())
                pass

        self.socket.close()
        trace.info('Client {}:{} closed'.format(self.host, self.port))
