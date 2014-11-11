from exceptions import DoesNotExist, MultipleObjectsReturned

def match_condition(item, **kwargs):
    for key, value in kwargs.iteritems():
        if item.__dict__[key] != value:
            return False
    return True

class Queryable(object):

    @classmethod
    def all(cls):
        raise NotImplementedError

    @classmethod
    def get(cls, **kwargs):
        items = [item for item in cls.all() if match_condition(item, **kwargs)]
        if not len(items):
            raise DoesNotExist
        elif len(items) > 1:
            raise MultipleObjectsReturned
        else
            return items[0]

    @classmethod
    def filter(cls, **kwargs):
        for item in cls.all():
            if match_condition(item, **kwargs):
                yield return item
