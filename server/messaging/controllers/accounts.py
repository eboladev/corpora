import hashlib
from datetime import datetime
from messaging.entity import SMAPResponse
from messaging.models import User

def login(request):
    try:
        username = request['user']
        password = request['password']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='params_invalid'))
        return

    request.db.connect()
    with request.db.transaction():
        try:
            user = User.get(User.username == username)
        except User.DoesNotExist:
            request.agent.queue.put(SMAPResponse('error', reason='not_registered'))
            return

        hash_value = hashlib.sha1(password).hexdigest()
        if user.password != hash_value:
            request.agent.queue.put(SMAPResponse('error', reason='password_invalid'))
            return
        elif user.is_active:
            request.agent.queue.put(SMAPResponse('error', reason='already_logged_in'))
            return

        user.is_active = True
        user.last_seen = datetime.now()
        user.save()

        request.agent.register(user)
        request.session['user'] = user
        request.agent.queue.put(SMAPResponse('success', reason='logged_in'))

def logout(request):
    try:
        username = request.session['user']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='not_logged_in'))

    request.db.connect()
    with request.db.transaction():
        user = User.get(User.username == username)
        user.is_active = False
        user.last_seen = datetime.now()
        user.save()

        request.session['user'] = None
        request.agent.queue.put(SMAPResponse('success', reason='logged_out'))


def register(request):
    try:
        username = request['user']
        password = request['password']
        email = request['email']
    except KeyError:
        request.agent.queue.put(SMAPResponse('error', reason='params_invalid'))
        return

    request.db.connect()
    with request.db.transaction():
        if User.select().where(User.username == username).count() > 0:
            request.agent.queue.put(SMAPResponse('error', reason='already_registered'))
            return

        user = User()
        user.username = username
        user.password = hashlib.sha1(password).hexdigest()
        user.email = email
        user.last_seen = datetime.now()

        user.save()
        request.agent.queue.put(SMAPResponse('success', reason='registered'))
