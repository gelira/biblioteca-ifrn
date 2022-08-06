from .base import BasePermission

class PromoverBolsistaPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def has_permission(self, request, view):
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        usuario = self.cliente_redis.get(_id)
        return 'bolsista.promover' in usuario['lista_permissoes']
