from rest_framework.permissions import BasePermission

from ..cliente_redis import ClienteRedis

class AbonarSuspensaoPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def __init__(self):
        self.cliente_redis = ClienteRedis()

    def has_permission(self, request, view):
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        usuario = self.cliente_redis.get(_id)
        return 'suspensao.abonar' in usuario['lista_permissoes']
