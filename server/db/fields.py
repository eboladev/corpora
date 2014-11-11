import resolver
from query import Queryable

class Field(object):

    def __init__(self, null=True, default=None, **options):
        self.name = ''  # Not initialized yet
        self.null = null
        self.default = default

    def __get__(self, obj, type):
        pass

    def __set__(self, obj, value):
        pass


class RelatedField(Field):

    def __init__(self, othermodel, related_name=None, **options):
        super(Field, self).__init__(**options)
        resolver.register_resolve(othermodel, self._resolve)

    def _resolve(othermodel):
        pass


class OneToOneField(RelatedField):

    def __get__(self, obj, type):
        pass

    def __set__(self, obj, value):
        pass


class ForeignKey(RelatedField):

    def __get__(self, obj, type):
        pass

    def __set__(self, obj, value):
        pass


class ManyToManyField(RelatedField, Queryable):

    def __get__(self, obj, type):
        pass

    def __set__(self, obj, value):
        pass
