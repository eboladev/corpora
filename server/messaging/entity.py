import json

def load(data):
    data = data.decode('utf-8', errors='replace')
    return json.loads(data)

def dump(entity):
    return json.dumps(entity, ensure_ascii=False).encode('utf-8')

def response(status, **params):
    params['status'] = status
    return params
