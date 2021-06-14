from django.http.response import JsonResponse

from ..services import AutenticacaoService
from .base import BaseMiddleware

class AutenticacaoMiddleware(BaseMiddleware):
    def process_request(self, request):
        try:
            request.META['_id'] = self.autenticar_request(request)
            return self.get_response(request)

        except Exception as e:
            arg = e.args[0]
            
            if isinstance(arg, dict):
                return JsonResponse(
                    arg.get('error'), 
                    status=arg.get('status', 500)
                )
            
            raise e

    def autenticar_request(self, request):
        token = request.headers.get('Authorization')
        
        if token is None:
            return None
        
        return AutenticacaoService.verificar_token(token)
