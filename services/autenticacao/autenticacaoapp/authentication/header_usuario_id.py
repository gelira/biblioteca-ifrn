from rest_framework.authentication import BaseAuthentication

from ..models import Usuario

class HeaderUsuarioIdAutenticacao(BaseAuthentication):
    def authenticate(self, request):
        usuario_id = request.META.get('HTTP_X_USUARIO_ID')

        usuario = Usuario.objects.filter(_id=usuario_id).first()
        if not usuario:
            return None

        return usuario.user, None
