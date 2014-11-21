
ROUTE_PATTERNS = (
    ('login', 'accounts.login'),
    ('logout', 'accounts.logout'),
    ('register', 'accounts.register'),
    ('join', 'channels.join'),
    ('leave', 'channels.leave'),
    ('message', 'channels.message'),
    ('share', 'deposit.share'),
)

def route_request(request):
    for verb, view in ROUTE_PATTERNS:
        if request['action'] == verb:
            module, _, func = view.partition('.')
            __import__(module, globals(), locals()).__dict__[func](request)
            return
