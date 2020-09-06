from django.http.response import JsonResponse

import os
import requests
from requests.exceptions import ConnectionError, Timeout
from rest_framework.exceptions import AuthenticationFailed

from .base import BaseMiddleware

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

class AutenticacaoMiddleware(BaseMiddleware):
    def process_request(self, request):
        try:
            request.META['_id'] = self.autenticar_request(request)
            return self.get_response(request)

        except (ConnectionError, Timeout):
            return JsonResponse({ 'detail': 'Serviço demorou muito para responder' }, status=408)

        except AuthenticationFailed:
            return JsonResponse({ 'detail': 'Token inválido' }, status=401)

    def autenticar_request(self, request):
        token = request.headers.get('Authorization')
        if token is None:
            return None
        res = requests.get(AUTENTICACAO_SERVICE_URL + '/verificar', timeout=5, headers={ 
            'Authorization': 'JWT {}'.format(token) 
        })
        if res.ok:
            return res.json()['_id']
        raise AuthenticationFailed
