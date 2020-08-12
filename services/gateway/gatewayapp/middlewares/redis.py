import os
import requests
from rest_framework.exceptions import AuthenticationFailed

from ..cliente_redis import ClienteRedis
from .base import BaseMiddleware

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

class RedisMiddleware(BaseMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.con = ClienteRedis()

    def process_request(self, request):
        chave = request.META['_id']
        if not self.con.exist(chave):
            res = requests.get(AUTENTICACAO_SERVICE_URL + '/informacoes', timeout=5, headers={ 
                'Authorization': 'JWT {}'.format(request.headers['Authorization']) 
            })
            if not res.ok:
                raise AuthenticationFailed
            self.con.store(chave, res.text)
        return self.get_response(request)
