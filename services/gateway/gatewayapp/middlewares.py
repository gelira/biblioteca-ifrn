import requests

class AutenticacaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.META['_id'] = self.autenticar_request(request)
        return self.get_response(request)

    def autenticar_request(self, request):
        token = request.headers.get('Authorization')
        res = requests.post('http://127.0.0.1:8001/verificar', json={ 'token': token })
        if res.ok:
            return res.json()['_id']
        return None
