from query import Queryable

class Model(Queryable):

    def __init__(self, **kwargs):
        pass

    @classmethod
    def all(cls):
        pass

    def save(self):
        pass
