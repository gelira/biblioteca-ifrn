from rest_framework.authentication import BaseAuthentication

from ..services import AutenticacaoService

class HeaderUsuarioIdAutenticacao(BaseAuthentication):
    def authenticate(self, request):
        usuario = None

        usuario_id = request.META.get('HTTP_X_USUARIO_ID')
        if usuario_id is not None:
            save_cache = not request.META.get('redis_error')
            
            try:
                usuario = AutenticacaoService.informacoes_usuario(usuario_id=usuario_id, save_cache=save_cache)
            except:
                pass
            
        if usuario is None:
            return None
            
        return usuario, None
