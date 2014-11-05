import json

class SMAPRequest(dict):

    def __init__(self, data, host=None, port=None, session=None):
        data = data.decode('utf-8', errors='replace')
        params = json.loads(data)
        super(SMAPRequest, self).__init__(self, **params)

        self.action = params['action']
        self.host = host
        self.port = port
        self.session = session

class SMAPResponse(dict):

    def __init__(self, status, **params):
        params['status'] = status
        super(SMAPResponse, self).__init__(self, params)

    def __str__(self):
        return json.dumps(self, ensure_ascii=False).encode('utf-8')

    @property
    def status(self):
        return self['status']

    @status.setter
    def set_status(self, value):
        self['status'] = value
