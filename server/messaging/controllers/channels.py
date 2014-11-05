from messaging.entity import SMAPResponse

def connected(request):
    pass

def join(request):
    request.service.lock.acquire()
    channel = request['channel']
    user = request.session['user']
    request.service.channels[channel] = request.service.channels.get(channel, []) + [user]
    for u in request.service.channels[channel]:
        c = [client for client in request.service.clients if client.name == request.service.users[u]][0]
        c.queue.put(SMAPResponse("user", channel=channel, username=user))
    for client in request.service.clients:
        if client.name == request.session['id']:
            client.queue.put(SMAPResponse('success', reason='joined_channel', channel=channel))
    request.service.lock.release()

def leave(request):
    pass

def message(request):
    request.service.lock.acquire()
    channel = request['channel']
    user = request.session['user']
    for u in request.service.channels[channel]:
        c = [client for client in request.service.clients if client.name == request.service.users[u]][0]
        c.queue.put(SMAPResponse("message", channel=channel, username=user, content=request['content']))
    request.service.lock.release()

def disconnected(request):
    pass
