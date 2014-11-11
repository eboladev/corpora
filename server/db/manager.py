# Emulation of real database.
# Do not try this at home.
from threading import Lock

class ManagerBase(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(ManagerBase, cls).__call(*args, **kwargs)
        return cls.instance


class Manager(object):
    __metaclass__ = ManagerBase

    def __init__(self):
        self.lock = Lock()
        self.tables = {}

    def __enter__(self):
        self.lock.acquire()

    def __exit__(self):
        self.lock.release()

    def table(self, cls):
        if cls not in self.tables:
            self.tables[cls] = []
        return self.tables[cls]
