from ..services import AutenticacaoService
from .base import BaseMiddleware

class AutenticacaoMiddleware(BaseMiddleware):
    def process_request(self, request):
        request.META['_id'] = self.autenticar_request(request)
        return self.get_response(request)

    def autenticar_request(self, request):
        token = request.headers.get('Authorization')
        
        if token is None:
            return None
        
        data = AutenticacaoService.verificar_token(token)
        return data['_id']
