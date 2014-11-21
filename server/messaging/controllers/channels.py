import hashlib
from messaging.entity import SMAPResponse
from messaging.models import User, Channel, Message

def connected(request):
    pass

def join(request):
    try:
        username = request.session['user']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='not_logged_in'))
        return

    try:
        channel_name = request['channel']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='params_invalid'))
        return

    with request.db.transaction():
        user = User.get(User.username == username)

        try:
            channel = Channel.get(Channel.name == channel_name)
        except Channel.DoesNotExist:
            channel = Channel(name=channel_name, owner=user)
            channel.save()

        if channel.is_private and channel.owner != user:
            request.agent.queue.put(SMAPResponse('error', reason='forbidden'))
            return

        channel.add_user(user)
        for u in channel.users:
            request.agent.dispatch(u.username, SMAPResponse('user',
                channel=channel.name, username=username, email=hashlib.md5(user.email).hexdigest()))

        request.agent.queue.put(SMAPResponse('success', reason='joined_channel', channel=channel.name))

def leave(request):
    try:
        username = request.session['user']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='not_logged_in'))
        return

    try:
        channel_name = request['channel']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='params_invalid'))
        return

    with request.db.transaction():
        user = User.get(User.username == username)

        try:
            channel = Channel.get(Channel.name == channel_name)
        except Channel.DoesNotExist:
            request.agent.queue.put(SMAPResponse('error', reason='invalid_channel'))
            return

        if channel.contains_user(user):
            channel.remove_user(user)
            for u in channel.users.iterator():
                request.agent.dispatch(u.username, SMAPResponse('left', channel=channel.name, username=username))

            request.agent.queue.put(SMAPResponse('success', reason='left_channel', channel=channel.name))
        else:
            request.agent.queue.put(SMAPResponse('error', reason='not_joined_yet'))


def message(request):
    try:
        username = request.session['user']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='not_logged_in'))
        return

    try:
        channel_name = request['channel']
        content = request['content']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='params_invalid'))
        return

    with request.db.transaction():
        user = User.get(User.username == username)

        try:
            channel = Channel.get(Channel.name == channel_name)
        except Channel.DoesNotExist:
            request.agent.queue.put(SMAPResponse('error', reason='invalid_channel'))
            return

        if channel.contains_user(user):
            Message.create(user=user, channel=channel, content=content)
            for u in channel.users:
                request.agent.dispatch(u.username, SMAPResponse('message', channel=channel.name, username=username, content=content))
        else:
            request.agent.queue.put(SMAPResponse('error', reason='not_joined_yet'))


def disconnected(request):
    pass
