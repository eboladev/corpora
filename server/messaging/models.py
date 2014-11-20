import config
import peewee as models

db = models.SqliteDatabase(config.DATABASE_NAME)

class BaseModel(models.Model):
    class Meta:
        database = db


class User(BaseModel):

    username = models.CharField(index=True, unique=True, max_length=32)
    email = models.CharField()
    is_active = models.BooleanField(default=False)
    last_seen = models.DateTimeField()

    @property
    def channels(self):
        return User.select().join(UserChannel).join(Channel).where(UserChannel.user == self)


class Channel(BaseModel):

    name = models.CharField(index=True, unique=True, max_length=32)
    is_private = models.BooleanField(default=False)

    @property
    def users(self):
        return Channel.select().join(UserChannel).join(User).where(UserChannel.channel == self)


class Message(BaseModel):

    user = models.ForeignKeyField(User)
    channel = models.ForeignKeyField(Channel)
    content = models.TextField()
    timestamp = models.DateTimeField()


class UserChannel(BaseModel):

    user = models.ForeignKeyField(User)
    channel = models.ForeignKeyField(Channel)

    class Meta:
        primary_key = models.CompositeKey('user', 'channel')


def create_tables():
    db.connect()
    db.create_tables([User, Channel, Message, UserChannel])
