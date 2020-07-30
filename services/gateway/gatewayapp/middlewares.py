from django.http.response import JsonResponse

import os
import requests
from requests.exceptions import ConnectionError, Timeout
from rest_framework.exceptions import AuthenticationFailed

from .cliente_redis import ClienteRedis

ALLOW_URLS = [
    '/autenticacao/token',
    '/autenticacao/verificar'
]

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

class AutenticacaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if request.path not in ALLOW_URLS:
                request.META['_id'] = self.autenticar_request(request)
            return self.get_response(request)

        except KeyError:
            return JsonResponse({ 'detail': 'Token não especificado' }, status=401)

        except (ConnectionError, Timeout):
            return JsonResponse({ 'detail': 'Serviço demorou muito para responder' }, status=408)

        except AuthenticationFailed:
            return JsonResponse({ 'detail': 'Token inválido' }, status=401)

    def autenticar_request(self, request):
        token = request.headers['Authorization']
        res = requests.get(AUTENTICACAO_SERVICE_URL + '/verificar', timeout=5, headers={ 
            'Authorization': 'JWT {}'.format(token) 
        })
        if res.ok:
            return res.json()['_id']
        raise AuthenticationFailed

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
