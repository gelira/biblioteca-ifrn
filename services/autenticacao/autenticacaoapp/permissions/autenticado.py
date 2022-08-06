from django.contrib.auth.models import AnonymousUser

from .base import BasePermission

class AutenticadoPermissao(BasePermission):
    message = 'Usuário não autenticado'

    def has_permission(self, request, view):
        if request.user is None or isinstance(request.user, AnonymousUser):
            return False
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        return self.cliente_redis.exist(_id)
