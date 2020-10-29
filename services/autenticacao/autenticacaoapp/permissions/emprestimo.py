from rest_framework.permissions import BasePermission

from ..cliente_redis import ClienteRedis

class FazerEmprestimoPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def __init__(self):
        self.cliente_redis = ClienteRedis()

    def has_permission(self, request, view):
        _id = str(request.user.usuario._id)
        usuario = self.cliente_redis.get(_id)
        return 'emprestimo.fazer' in usuario['lista_permissoes']
