from django.http.response import JsonResponse

import requests
from requests.exceptions import ConnectionError, Timeout
from rest_framework.exceptions import AuthenticationFailed

class AutenticacaoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
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
        res = requests.post('http://127.0.0.1:8001/verificar', timeout=5, json={ 'token': token })
        if res.ok:
            return res.json()['_id']
        raise AuthenticationFailed
