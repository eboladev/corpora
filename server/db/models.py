import fields
from query import Queryable
from resolver import register_model

class ModelBase(type):

    def __new__(cls, name, bases, attrs):
        super_new = super(ModelBase, cls).__new__

        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            super_new(cls, name, bases, attrs)

        # Class creation
        new_class = super_new(cls, name, bases, attrs)
        return new_class

class Model(Queryable):
    __metaclass__ = ModelBase

    def __new__(cls):
        for field in cls.__dict__:
            if not isinstance(field, fields.Field):
                continue

            # Do something with fields

        register_model(cls)

    def __init__(self, **kwargs):
        pass

    @classmethod
    def all(cls):
        pass

    def save(self):
        pass
