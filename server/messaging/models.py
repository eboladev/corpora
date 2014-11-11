from db.models import Model
from db.fields import Field, ManyToManyField

class User(Model):
    username = Field()
    email = Field()
    # channels = [related field]

class Channel(Model):
    name = Field()
    private = Field()
    users = ManyToManyField('User')
