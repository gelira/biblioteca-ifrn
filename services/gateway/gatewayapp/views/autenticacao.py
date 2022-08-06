import os

from .base import BaseProxyView

AUTENTICACAO_SERVICE_URL = os.getenv('AUTENTICACAO_SERVICE_URL')

class AutenticacaoProxyView(BaseProxyView):
    upstream = AUTENTICACAO_SERVICE_URL

    def get_request_headers(self):
        headers = super(BaseProxyView, self).get_request_headers()
        headers.pop('X-Usuario-Id', None)
        
        authorization = headers.get('Authorization')

        if authorization is not None:
            headers['Authorization'] = f'JWT {authorization}'
        
        return headers
