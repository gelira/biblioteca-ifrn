from django.http.response import JsonResponse

from ..services import AutenticacaoService
from ..cliente_redis import ClienteRedis
from .base import BaseMiddleware

class RedisMiddleware(BaseMiddleware):
    def __init__(self, get_response):
        super().__init__(get_response)
        self.con = ClienteRedis()

    def process_request(self, request):
        chave = request.META.get('_id')

        if chave is not None:
            if not self.con.exist(chave):
                try:
                    informacoes = AutenticacaoService.informacoes_usuario(chave)
                    self.con.store(chave, informacoes)
                
                except Exception as e:
                    arg = e.args[0]
            
                    if isinstance(arg, dict):
                        return JsonResponse(
                            arg.get('error'), 
                            status=arg.get('status', 500)
                        )
                    
                    raise e

        return self.get_response(request)
