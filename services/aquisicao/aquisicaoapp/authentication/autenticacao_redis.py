from rest_framework.authentication import BaseAuthentication

from ..cliente_redis import ClienteRedis

class RedisAutenticacao(BaseAuthentication):
    def authenticate(self, request):
        cliente_redis = ClienteRedis()
        usuario = None

        usuario_id = request.META.get('HTTP_X_USUARIO_ID')
        if usuario_id is not None:
            try:
                usuario = cliente_redis.get(usuario_id)
            except:
                pass
            
        if usuario is None:
            return None
            
        return usuario, None
