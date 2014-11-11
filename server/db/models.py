import fields
import resolver
from query import Queryable

class ModelBase(type):

    def __new__(cls, name, bases, attrs):
        new_class = super(ModelBase, cls).__new__(cls, name, bases, attrs)
        local_fields = []

        for attr, field in attrs.iteritems():
            if isinstance(field, fields.Field):
                field.name = attr
                local_fields.append(attr)

        cls.local_fields = tuple(local_fields)
        resolver.register_model(cls)
        return new_class

class Model(Queryable):
    __metaclass__ = ModelBase

    def __init__(self, **kwargs):
        self._state = {}
        for key, value in kwargs:
            setattr(self, key, value)

    @classmethod
    def all(cls):
        pass

    def save(self):
        pass
