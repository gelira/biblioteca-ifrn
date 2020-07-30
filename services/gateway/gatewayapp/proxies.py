import os
from django.http.response import JsonResponse
from revproxy.views import ProxyView
from urllib3.exceptions import MaxRetryError

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

class BaseProxy(ProxyView):
    def dispatch(self, request, path):
        try:
            return super().dispatch(request, path)
        except MaxRetryError:
            return JsonResponse({ 'detail': 'Serviço indisponível' }, status=408)

    def get_request_headers(self):
        headers = super().get_request_headers()
        headers.pop('Authorization', None)
        usuario_id = self.request.META.get('_id')
        if usuario_id is not None:
            headers['X-Usuario-Id'] = usuario_id
        return headers

class AutenticacaoProxy(BaseProxy):
    upstream = AUTENTICACAO_SERVICE_URL

    def get_request_headers(self):
        headers = super(BaseProxy, self).get_request_headers()
        authorization = headers.get('Authorization')
        if authorization is not None:
            headers['Authorization'] = 'JWT {}'.format(authorization)
        return headers
