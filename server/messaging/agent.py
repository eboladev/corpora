import config
import models
import Queue
import socket
import threading
import trace
from controllers import routes
from entity import SMAPRequest, SMAPResponse

class MessagingAgent(threading.Thread):

    def __init__(self, service, id, conn, host, port):
        super(MessagingAgent, self).__init__()
        self.daemon = True
        self.name = 'messaging-{}'.format(id)
        self.queue = Queue.Queue()
        self.socket = conn
        self.service = service
        self.host = host
        self.port = port
        self.session = { "id": self.name }
        self.db = models.create_database()

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
                self.handle_response(response)
                response = None

            try:
                data = self.socket.recv(config.MESSAGING_BUFFER_SIZE)
                if data:
                    buf += data
                    end = buf.find('\n')
                    if end >= 0:
                        request = buf[:end].strip()
                        buf = buf[end+2:]
                else:
                    break   # Connection closed
            except socket.timeout: pass

            if request:
                self.handle_request(request)
                request = ''

        self.socket.close()
        trace.info('Client {}:{} closed'.format(self.host, self.port))

    def handle_response(self, response):
        data = str(response) + '\n'
        trace.info('Response', response.status.upper(), 'length', len(data))
        self.socket.sendall(data)

    def handle_request(self, data):
        try:
            request = SMAPRequest(data, self)
            trace.info('Request', request.action.upper(), 'length', len(data))
        except (ValueError, KeyError):
            trace.info('Request length', len(data))
            self.queue.put(SMAPResponse('error', reason='bad_request'))
        else:
            routes.route_request(request)

    def register(self, username):
        self.user = username

    def dispatch(self, username, response):
        self.service.dispatch(self, username, response)
