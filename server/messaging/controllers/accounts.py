from messaging.entity import SMAPResponse

def login(request):
    request.service.lock.acquire()
    user = request['user']
    if user not in request.service.users:
        request.service.users[user] = request.session['id']
        request.session['user'] = user
        for client in request.service.clients:
            if client.name == request.session['id']:
                client.queue.put(SMAPResponse('success', reason='logged_in'))
    else:
        for client in request.service.clients:
            if client.name == request.session['id']:
                client.queue.put(SMAPResponse('error', reason='name_in_use'))
    request.service.lock.release()

def logout(request):
    pass
