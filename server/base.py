import threading

class BaseService(threading.Thread):

    def __init__(self, name=None):
        super(BaseService, self).__init__(name=name)
        self.daemon = True

    def alive(self):
        return True

    def wait(self):
        return ()

    def handle(self):
        raise NotImplementedError

    def run(self):
        print('Starting %s service...' % self.name)
        while self.alive():
            request = self.wait()
            self.handle(*request)
