import os
import requests
from rest_framework.exceptions import AuthenticationFailed

from ..cliente_redis import ClienteRedis

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

ALLOW_URLS = [
    '/autenticacao/token',
    '/autenticacao/verificar'
]

class RedisMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.con = ClienteRedis()

    def __call__(self, request):
        if request.path not in ALLOW_URLS:
            self.check_redis(request)
        return self.get_response(request)

    def check_redis(self, request):
        chave = request.META['_id']
        if not self.con.exist(chave):
            res = requests.get(AUTENTICACAO_SERVICE_URL + '/informacoes', timeout=5, headers={ 
                'Authorization': 'JWT {}'.format(request.headers['Authorization']) 
            })
            if not res.ok:
                raise AuthenticationFailed
            self.con.store(chave, res.text)
