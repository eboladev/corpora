import threading

class BaseService(threading.Thread):

    def __init__(self, name=None):
        super.__init__(self, name=name)
        self.daemon = False
        self.event = None

    def run(self):
        raise NotImplementedError
