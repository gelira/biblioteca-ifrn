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
                token = request.headers.get('Authorization')
                informacoes = AutenticacaoService.informacoes_usuario(token)
                self.con.store(chave, informacoes)

        return self.get_response(request)
