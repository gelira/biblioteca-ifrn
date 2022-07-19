from rest_framework.permissions import BasePermission

from ..cliente_redis import ClienteRedis

class AutenticadoPermissao(BasePermission):
    message = 'Usuário não autenticado'

    def __init__(self):
        self.cliente_redis = ClienteRedis()

    def has_permission(self, request, view):
        if request.user is None:
            return False
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        return self.cliente_redis.exist(_id)
