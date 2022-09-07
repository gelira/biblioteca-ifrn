from rest_framework.permissions import BasePermission

class GerenciarPerfilPermissao(BasePermission):
    message = 'Você não tem permissão para realizar essa ação'

    def has_permission(self, request, view):
        return request.user.usuario.permissoes\
            .filter(permissao__codigo='perfil.gerenciar').exists()
