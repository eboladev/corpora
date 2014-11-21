import config
import peewee as models

db = models.SqliteDatabase(config.DATABASE_NAME)

class BaseModel(models.Model):
    class Meta:
        database = db


class User(BaseModel):

    username = models.CharField(index=True, unique=True, max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField()
    is_active = models.BooleanField(default=False)
    last_seen = models.DateTimeField()

    @property
    def channels(self):
        return User.select().join(UserChannel).join(Channel).where(UserChannel.user == self)


class Channel(BaseModel):

    owner = models.ForeignKeyField(User)
    name = models.CharField(index=True, unique=True, max_length=32)
    is_private = models.BooleanField(default=False)

    @property
    def users(self):
        return Channel.select().join(UserChannel).join(User).where(UserChannel.channel == self)

    def add_user(self, user):
        try:
            return UserChannel(user=user, channel=self).save()
        except models.IntegrityError:
            return False

    def remove_user(self, user):
        return UserChannel.delete().where((UserChannel.user == user) & (UserChannel.channel == self)).execute()

    def contains_user(self, user):
        return (UserChannel.select().where((UserChannel.user == user) & (UserChannel.channel == self)).count() > 0)


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


def create_database():
    return models.SqliteDatabase(config.DATABASE_NAME, threadlocals=True)

def create_tables():
    db.connect()
    db.create_tables([User, Channel, Message, UserChannel])
