from rest_framework.permissions import BasePermission

from ..cliente_redis import ClienteRedis

class ConsultarUsuarioPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def __init__(self):
        self.cliente_redis = ClienteRedis()

    def has_permission(self, request, view):
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        usuario = self.cliente_redis.get(_id)
        return 'usuario.consultar' in usuario['lista_permissoes']

class SuspenderUsuarioPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def __init__(self):
        self.cliente_redis = ClienteRedis()

    def has_permission(self, request, view):
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        usuario = self.cliente_redis.get(_id)
        return 'usuario.suspender' in usuario['lista_permissoes']

class AbonarUsuarioPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def __init__(self):
        self.cliente_redis = ClienteRedis()

    def has_permission(self, request, view):
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        usuario = self.cliente_redis.get(_id)
        return 'usuario.abonar' in usuario['lista_permissoes']
