from .base import BasePermission

class FazerEmprestimoPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def has_permission(self, request, view):
        _id = request.user['_id'] if isinstance(request.user, dict) else str(request.user.usuario._id)
        usuario = self.cliente_redis.get(_id)
        return 'emprestimo.fazer' in usuario['lista_permissoes']
